from fastapi import HTTPException
from sqlalchemy.orm import Session

from .bw_parser import ParsedBW2Workbook
from .models import Activity, Exchange, MaterialImpact, ElectricityImpact
from . import models


def get_activity_by_name(
    db: Session,
    activity_name: str,
    partner_id: str | None = None
):
    # First see if the given partner (if given) has a partner-specific activity associated with it
    if partner_id:
        partner_activity = (
            db.query(models.Activity)
            .filter(
                models.Activity.name == activity_name,
                models.Activity.partner_id == partner_id
            )
            .first()
        )

        if partner_activity:
            return partner_activity

    # Check if a base activity exists as a fallback
    base_activity = (
        db.query(models.Activity)
        .filter(
            models.Activity.name == activity_name,
            models.Activity.partner_id == None
        )
        .first()
    )

    if not base_activity:
        raise HTTPException(
            status_code=404,
            detail=f"Activity '{activity_name}' not found"
        )

    return base_activity


def calculate_activity_impact_recursive(
    db: Session,
    activity_name: str,
    partner_id: str | None = None,
    visited: set | None = None
) -> float:

    if visited is None:
        visited = set()

    # Circular dependency protection
    if activity_name in visited:
        raise HTTPException(
            status_code=400,
            detail=f"Circular dependency detected for '{activity_name}'"
        )

    visited.add(activity_name)

    activity = get_activity_by_name(
        db,
        activity_name,
        partner_id
    )

    total_impact = 0.0

    for exchange in activity.exchanges:

        input_name = exchange.input_name
        amount = exchange.amount

        # ============================================
        # MATERIAL LOOKUP
        # ============================================

        material = (
            db.query(models.MaterialImpact)
            .filter(models.MaterialImpact.name == input_name)
            .first()
        )

        if material:
            total_impact += amount * material.impact_factor
            continue

        # ============================================
        # ELECTRICITY LOOKUP
        # ============================================

        electricity = (
            db.query(models.ElectricityImpact)
            .filter(models.ElectricityImpact.name == input_name)
            .first()
        )

        if electricity:
            total_impact += amount * electricity.impact_factor
            continue

        # ============================================
        # RECURSIVE ACTIVITY LOOKUP
        # ============================================

        nested_impact = calculate_activity_impact_recursive(
            db=db,
            activity_name=input_name,
            partner_id=partner_id,
            visited=visited.copy()
        )

        total_impact += amount * nested_impact

    return total_impact


def persist_parsed_workbook(
    db: Session,
    parsed: ParsedBW2Workbook,
    partner_id: str | None = None,
):
    """
    Persist parsed workbook contents into the database.
    """

    # --------------------------------------------------------
    # Activities + exchanges
    # --------------------------------------------------------

    for parsed_activity in parsed.activities:

        activity = Activity(
            name=parsed_activity.name,
            partner_id=partner_id,
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
    # Only inserted for Company A base dataset
    # --------------------------------------------------------

    if partner_id is None:

        for parsed_material in parsed.material_impacts:

            material = MaterialImpact(
                name=parsed_material.name,
                impact_factor=parsed_material.impact_factor,
            )

            db.add(material)

        # ----------------------------------------------------
        # Electricity impacts
        # ----------------------------------------------------

        for parsed_electricity in parsed.electricity_impacts:

            electricity = ElectricityImpact(
                name=parsed_electricity.name,
                impact_factor=parsed_electricity.impact_factor,
            )

            db.add(electricity)

    db.commit()