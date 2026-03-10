from typing import Literal

import pytest

from db.models import Engine, Hull, Weapon
from tests.conftest import DBDataAsDict


SHIP_IDS = [f"Ship-{i}" for i in range(1, 201)]

COMPONENT_CONFIG = {
    "weapons": Weapon.get_fields(),
    "hulls": Hull.get_fields(),
    "engines": Engine.get_fields(),
}


def _check_component(
    ship_name: str,
    original: DBDataAsDict,
    modified: DBDataAsDict,
    parametr_name: Literal["weapons", "hulls", "engines"],
) -> None:
    orig_ship = original.ships[ship_name]
    mod_ship = modified.ships[ship_name]

    orig_param = orig_ship[parametr_name]
    mod_param = mod_ship[parametr_name]

    if orig_param != mod_param:
        pytest.fail(f"{ship_name}, {mod_param}\nexpected {orig_param}, was {mod_param}")

    fields = COMPONENT_CONFIG[parametr_name]
    orig_comp = getattr(original, parametr_name)[orig_param]
    mod_comp = getattr(modified, parametr_name)[mod_param]

    diffs = []
    for f in fields:
        if orig_comp[f] != mod_comp[f]:
            diffs.append(f"{f}: expected {orig_comp[f]}, was {mod_comp[f]}")

    if diffs:
        pytest.fail(f"{ship_name}, {orig_param}\n" + "\n".join(diffs))


@pytest.mark.parametrize("ship_name", SHIP_IDS)
def test_weapon(ship_name: str, original_and_modified_db):
    original, modified = original_and_modified_db
    _check_component(ship_name, original, modified, "weapons")


@pytest.mark.parametrize("ship_name", SHIP_IDS)
def test_hull(ship_name: str, original_and_modified_db):
    original, modified = original_and_modified_db
    _check_component(ship_name, original, modified, "hulls")


@pytest.mark.parametrize("ship_name", SHIP_IDS)
def test_engine(ship_name: str, original_and_modified_db):
    original, modified = original_and_modified_db
    _check_component(ship_name, original, modified, "engines")
