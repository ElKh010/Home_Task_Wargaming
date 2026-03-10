import random

from db.models import Engine, Hull, Ship, Weapon


SHIP_COUNT = 200
WEAPON_COUNT = 20
HULL_COUNT = 5
ENGINE_COUNT = 6
VALUE_RANGE = (1, 20)


def rand_val() -> int:
    return random.randint(*VALUE_RANGE)


def create_weapons(count: int) -> list[Weapon]:
    weapon_result = [
        Weapon(
            weapon=f"Weapon-{i}",
            reload_speed=rand_val(),
            rotation_speed=rand_val(),
            diameter=rand_val(),
            power_volley=rand_val(),
            count=rand_val(),
        )
        for i in range(1, count + 1)
    ]
    return weapon_result


def create_hulls(count: int) -> list[Hull]:
    hull_result = [
        Hull(hull=f"Hull-{i}", armor=rand_val(), type=rand_val(), capacity=rand_val()) for i in range(1, count + 1)
    ]
    return hull_result


def create_engines(count: int) -> list[Engine]:
    engine_result = [Engine(engine=f"Engine-{i}", power=rand_val(), type=rand_val()) for i in range(1, count + 1)]
    return engine_result


def create_ships(
    count: int,
    weapons: list[Weapon],
    hulls: list[Hull],
    engines: list[Engine],
) -> list[Ship]:
    ship_result = [
        Ship(
            ship=f"Ship-{i}",
            weapon=random.choice(weapons).weapon,
            hull=random.choice(hulls).hull,
            engine=random.choice(engines).engine,
        )
        for i in range(1, count + 1)
    ]
    return ship_result
