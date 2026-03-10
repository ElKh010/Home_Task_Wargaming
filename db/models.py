from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Weapon(Base):
    __tablename__ = "weapons"

    weapon: Mapped[str] = mapped_column(Text, primary_key=True)
    reload_speed: Mapped[int] = mapped_column(Integer)
    rotation_speed: Mapped[int] = mapped_column(Integer)
    diameter: Mapped[int] = mapped_column(Integer)
    power_volley: Mapped[int] = mapped_column(Integer)
    count: Mapped[int] = mapped_column(Integer)

    def to_dict(self) -> dict:
        return {
            "reload_speed": self.reload_speed,
            "rotation_speed": self.rotation_speed,
            "diameter": self.diameter,
            "power_volley": self.power_volley,
            "count": self.count,
        }

    @staticmethod
    def get_fields() -> list[str]:
        return [c.name for c in Weapon.__table__.columns if not c.primary_key]


class Hull(Base):
    __tablename__ = "hulls"

    hull: Mapped[str] = mapped_column(Text, primary_key=True)
    armor: Mapped[int] = mapped_column(Integer)
    type: Mapped[int] = mapped_column(Integer)
    capacity: Mapped[int] = mapped_column(Integer)

    def to_dict(self) -> dict:
        return {
            "armor": self.armor,
            "type": self.type,
            "capacity": self.capacity,
        }

    @staticmethod
    def get_fields() -> list[str]:
        return [c.name for c in Hull.__table__.columns if not c.primary_key]


class Engine(Base):
    __tablename__ = "engines"

    engine: Mapped[str] = mapped_column(Text, primary_key=True)
    power: Mapped[int] = mapped_column(Integer)
    type: Mapped[int] = mapped_column(Integer)

    def to_dict(self) -> dict:
        return {
            "power": self.power,
            "type": self.type,
        }

    @staticmethod
    def get_fields() -> list[str]:
        return [c.name for c in Engine.__table__.columns if not c.primary_key]


class Ship(Base):
    __tablename__ = "ships"

    ship: Mapped[str] = mapped_column(Text, primary_key=True)
    weapon: Mapped[str] = mapped_column(ForeignKey("weapons.weapon"))
    hull: Mapped[str] = mapped_column(ForeignKey("hulls.hull"))
    engine: Mapped[str] = mapped_column(ForeignKey("engines.engine"))

    def to_dict(self) -> dict:
        return {
            "weapons": self.weapon,
            "hulls": self.hull,
            "engines": self.engine,
        }
