from pydantic import BaseModel


class ImpactResponse(BaseModel):
    activity_name: str
    partner_id: str | None
    total_impact: float
    unit: str = "kg CO2"