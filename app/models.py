from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint
)

from sqlalchemy.orm import relationship

from .database import Base


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)

    # Activity names are not globally unique because
    # different partners may define similarly named recipes.
    name = Column(String, nullable=False)

    # None = Company A base data
    # otherwise owned by uploaded partner dataset
    partner_id = Column(String, nullable=True)

    exchanges = relationship(
        "Exchange",
        back_populates="activity",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint(
            "name",
            "partner_id",
            name="uq_activity_partner"
        ),
    )


class Exchange(Base):
    __tablename__ = "exchanges"

    id = Column(Integer, primary_key=True, index=True)

    activity_id = Column(
        Integer,
        ForeignKey("activities.id"),
        nullable=False
    )

    # Name of referenced input:
    # - another activity
    # - material
    # - electricity source
    input_name = Column(String, nullable=False)

    amount = Column(Float, nullable=False)

    unit = Column(String, nullable=True)

    activity = relationship(
        "Activity",
        back_populates="exchanges"
    )


class MaterialImpact(Base):
    __tablename__ = "material_impacts"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String,
        unique=True,
        nullable=False
    )

    # kg CO2 / kg
    impact_factor = Column(
        Float,
        nullable=False
    )


class ElectricityImpact(Base):
    __tablename__ = "electricity_impacts"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String,
        unique=True,
        nullable=False
    )

    # kg CO2 / kWh
    impact_factor = Column(
        Float,
        nullable=False
    )