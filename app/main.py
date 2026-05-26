from fastapi import Depends, FastAPI, UploadFile, File
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .seed import bootstrap_company_a_data
from .database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

bootstrap_company_a_data()
    
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
    
@app.get("/materials")
def list_material_impacts(
    db: Session = Depends(get_db)
):
    """
    Debug/helper endpoint to inspect material impacts.
    """

    materials = db.query(models.MaterialImpact).all()

    return {
        "count": len(materials),
        "materials": [
            {
                "id": material.id,
                "name": material.name,
                "impact_factor": material.impact_factor
            }
            for material in materials
        ]
    }


@app.get("/electricity")
def list_electricity_impacts(
    db: Session = Depends(get_db)
):
    """
    Debug/helper endpoint to inspect electricity impacts.
    """

    electricity_sources = db.query(models.ElectricityImpact).all()

    return {
        "count": len(electricity_sources),
        "electricity_sources": [
            {
                "id": source.id,
                "name": source.name,
                "impact_factor": source.impact_factor
            }
            for source in electricity_sources
        ]
    }
    
@app.get("/activities")
def list_activities(
    partner_id: str | None = None,
    db: Session = Depends(get_db)
):
    """
    Debug/helper endpoint to inspect loaded activities.
    """

    query = db.query(models.Activity)

    # Show partner-visible activities:
    # - shared Company A activities
    # - partner-owned activities
    if partner_id:
        activities = query.filter(
            (models.Activity.partner_id == None) |
            (models.Activity.partner_id == partner_id)
        ).all()

    # Otherwise only Company A base activities
    else:
        activities = query.filter(
            models.Activity.partner_id == None
        ).all()

    return {
        "count": len(activities),
        "activities": [
            {
                "id": activity.id,
                "name": activity.name,
                "partner_id": activity.partner_id,
                "exchange_count": len(activity.exchanges),

                "exchanges": [
                    {
                        "id": exchange.id,
                        "input_name": exchange.input_name,
                        "amount": exchange.amount,
                        "unit": exchange.unit
                    }
                    for exchange in activity.exchanges
                ]
            }
            for activity in activities
        ]
    }


# =========================================================
# PART 1 — IMPACT CALCULATION
# =========================================================

@app.get(
    "/activities/{activity_name}/impact",
    response_model=schemas.ImpactResponse
)
def calculate_activity_impact(
    activity_name: str,
    partner_id: str | None = None,
    db: Session = Depends(get_db)
):
    """
        Gets the calculated activity of a given activity.
        
        - Looks for version associated with the partner id
        - Defaults to the base activity if the partner id doesn't have a unique version associated with it.
        - Case-sensitive
    """
    total_impact = crud.calculate_activity_impact_recursive(
        db=db,
        activity_name=activity_name,
        partner_id=partner_id
    )

    return schemas.ImpactResponse(
        activity_name=activity_name,
        partner_id=partner_id,
        total_impact=round(total_impact, 4)
    )


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
