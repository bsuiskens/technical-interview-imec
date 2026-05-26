from pathlib import Path
from dotenv import load_dotenv

import pandas as pd
from sqlalchemy.orm import Session

from .database import SessionLocal
from .bw_parser import parse_bw2_workbook
from .models import Activity, Exchange, MaterialImpact, ElectricityImpact
import os

load_dotenv()

DATA_PATH_ENV = os.getenv("SEED_DATA_PATH")
BASE_DATA_PATH = Path(DATA_PATH_ENV)


def bootstrap_company_a_data():
    """
    Seed Company A reference data if database is empty.

    This runs once at startup.
    """

    db: Session = SessionLocal()

    try:
        existing_activity = db.query(Activity).first()

        if existing_activity:
            print("Database already seeded.")
            return

        print("Seeding Company A database...")

        seed_company_a_data(db)

        print("Seeding complete.")

    finally:
        db.close()

def seed_company_a_data(db: Session):
    parsed = parse_bw2_workbook(BASE_DATA_PATH)

    # --------------------------------------------------------
    # Activities + exchanges
    # --------------------------------------------------------

    for parsed_activity in parsed.activities:
        activity = Activity(
            name=parsed_activity.name,
            partner_id=None,
        )

        db.add(activity)
        db.flush()

        for parsed_exchange in parsed_activity.exchanges:
            exchange = Exchange(
                activity_id=activity.id,
                input_name=parsed_exchange.input_name,
                amount=parsed_exchange.amount,
                unit=parsed_exchange.unit,
            )

            db.add(exchange)

    # --------------------------------------------------------
    # Material impacts
    # --------------------------------------------------------

    for parsed_material in parsed.material_impacts:
        material = MaterialImpact(
            name=parsed_material.name,
            impact_factor=parsed_material.impact_factor,
        )

        db.add(material)

    # --------------------------------------------------------
    # Electricity impacts
    # --------------------------------------------------------

    for parsed_electricity in parsed.electricity_impacts:
        electricity = ElectricityImpact(
            name=parsed_electricity.name,
            impact_factor=parsed_electricity.impact_factor,
        )

        db.add(electricity)

    db.commit()