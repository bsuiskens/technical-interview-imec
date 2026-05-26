from pathlib import Path
from dotenv import load_dotenv

from sqlalchemy.orm import Session

from .database import SessionLocal
from .bw_parser import parse_bw2_workbook
from .models import Activity
from .crud import persist_parsed_workbook
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

    persist_parsed_workbook(
        db=db,
        parsed=parsed,
        partner_id=None,
    )