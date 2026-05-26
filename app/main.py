from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import Base, engine, get_db

Base.metadata.create_all(bind=engine)


    
app = FastAPI(
    title="Wafer Impact API",
    description="Proof-of-concept API for recursive climate impact calculation.",
    version="0.1.0"
)

# VALIDATION / DEBUG ENDPOINTS

@app.get("/")
def root():
    return {
        "message": "Wafer Impact API running"
    }
    

@app.get("/activities")
def list_activities(
    partner_id: str | None = None,
    db: Session = Depends(get_db)
):
    """
    Debug/helper endpoint to inspect loaded activities.
    """

    # TODO:
    # - Return activities visible to partner
    # - Include base activities
    return {
        "status": "TODO"
    }



# =========================================================
# PART 1 — IMPACT CALCULATION
# =========================================================

@app.get("/activities/{activity_name}/impact")
def calculate_activity_impact(
    activity_name: str,
    partner_id: str | None = None,
    db: Session = Depends(get_db)
):
    """
    Resolve total climate impact recursively for an activity.

    Expected behavior:
    - Resolve exchanges recursively
    - Sum material/electricity impacts
    - Support partner-specific activities
    - Fall back to Company A base activities
    """

    # TODO:
    # 1. Lookup activity by:
    #    - partner_id + activity_name
    #    - fallback to base activity if not found
    #
    # 2. Resolve exchanges recursively
    #
    # 3. Detect circular dependencies
    #
    # 4. Sum total impact
    #
    # 5. Return structured response

    return {
        "status": "TODO",
        "activity_name": activity_name,
        "partner_id": partner_id
    }


# =========================================================
# PART 2 — PARTNER RECIPE UPLOAD
# =========================================================

@app.post("/partner-recipes/upload")
async def upload_partner_recipe(
    partner_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload and persist partner recipe Excel file.

    Expected behavior:
    - Parse uploaded Excel file
    - Validate sheet structure
    - Persist partner-owned activities/exchanges
    - Keep Company A data isolated
    """

    # TODO:
    # 1. Validate uploaded file type
    #
    # 2. Parse Excel workbook with pandas/openpyxl
    #
    # 3. Validate required columns/sheets
    #
    # 4. Store activities
    #
    # 5. Store exchanges
    #
    # 6. Associate all uploaded rows with partner_id
    #
    # 7. Handle duplicate uploads safely

    return {
        "status": "TODO",
        "partner_id": partner_id,
        "filename": file.filename
    }

