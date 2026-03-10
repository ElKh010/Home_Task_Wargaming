import random
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path

import pytest


sys.path.append(".")

from generate_data import (
    ENGINE_COUNT,
    HULL_COUNT,
    SHIP_COUNT,
    WEAPON_COUNT,
    create_engines,
    create_hulls,
    create_ships,
    create_weapons,
)

from db.database import DB_PATH, create_tables, open_session
from db.models import (
    Engine,
    Hull,
    Ship,
    Weapon,
)


MODIFIED_DB = "ships_modified.db"
VALUE_RANGE = (1, 20)


@dataclass
class DBDataAsDict:
    ships: dict[str, Ship] = field(default_factory=dict)
    weapons: dict[str, Weapon] = field(default_factory=dict)
    hulls: dict[str, Hull] = field(default_factory=dict)
    engines: dict[str, Engine] = field(default_factory=dict)


def read_all_tables(db_path: str) -> DBDataAsDict:
    data = DBDataAsDict()

    with open_session(db_path) as session:
        for w in session.query(Weapon).all():
            data.weapons[w.weapon] = w.to_dict()

        for h in session.query(Hull).all():
            data.hulls[h.hull] = h.to_dict()

        for e in session.query(Engine).all():
            data.engines[e.engine] = e.to_dict()

        for s in session.query(Ship).all():
            data.ships[s.ship] = s.to_dict()
    return data


def _randomize_one_param(session, model, pk_field: str, pk_value: str, fields: list[str]) -> None:
    obj = session.query(model).filter(getattr(model, pk_field) == pk_value).one()

    field_name = random.choice(fields)
    current = getattr(obj, field_name)

    new_val = random.randint(*VALUE_RANGE)
    while new_val == current:
        new_val = random.randint(*VALUE_RANGE)

    setattr(obj, field_name, new_val)


def randomize_database(db_path: str) -> None:
    with open_session(db_path) as session:
        ships = session.query(Ship).all()

        all_weapons = [w.weapon for w in session.query(Weapon).all()]
        all_hulls = [h.hull for h in session.query(Hull).all()]
        all_engines = [e.engine for e in session.query(Engine).all()]

        config = {
            "weapon": (Weapon, "weapon", Weapon.get_fields(), all_weapons),
            "hull": (Hull, "hull", Hull.get_fields(), all_hulls),
            "engine": (Engine, "engine", Engine.get_fields(), all_engines),
        }

        for ship in ships:
            key = random.choice(list(config.keys()))
            model, pk_field, fields, values = config[key]

            new_ship = random.choice(values)
            setattr(ship, key, new_ship)

            _randomize_one_param(session, model, pk_field, new_ship, fields)


@pytest.fixture(scope="session")
def original_and_modified_db(tmp_path_factory) -> tuple[DBDataAsDict, DBDataAsDict]:

    original = read_all_tables(DB_PATH)

    tmp_dir = tmp_path_factory.mktemp("db")
    modified_path = str(tmp_dir / MODIFIED_DB)
    shutil.copy2(DB_PATH, modified_path)
    randomize_database(modified_path)

    modified = read_all_tables(modified_path)

    return original, modified


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    if Path(DB_PATH).exists():
        Path(DB_PATH).unlink()

    create_tables(DB_PATH)

    weapons = create_weapons(WEAPON_COUNT)
    hulls = create_hulls(HULL_COUNT)
    engines = create_engines(ENGINE_COUNT)
    ships = create_ships(SHIP_COUNT, weapons, hulls, engines)

    with open_session(DB_PATH) as session:
        session.add_all(weapons + hulls + engines + ships)
