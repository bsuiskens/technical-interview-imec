from dataclasses import dataclass
from pathlib import Path
from typing import List

import pandas as pd


@dataclass
class ParsedExchange:
    input_name: str
    amount: float
    unit: str | None


@dataclass
class ParsedActivity:
    name: str
    exchanges: List[ParsedExchange]


@dataclass
class ParsedMaterialImpact:
    name: str
    impact_factor: float


@dataclass
class ParsedElectricityImpact:
    name: str
    impact_factor: float


@dataclass
class ParsedBW2Workbook:
    activities: List[ParsedActivity]
    material_impacts: List[ParsedMaterialImpact]
    electricity_impacts: List[ParsedElectricityImpact]

    
def parse_bw2_workbook(path: str | Path) -> ParsedBW2Workbook:
    """
    Main workbook parser entrypoint.
    """

    with pd.ExcelFile(path) as xls: #Ensures it terminates if it uses a tempfile that gets deleted during the operation

        activities = parse_activities_sheet(xls)

        material_impacts = (
            parse_material_impacts(xls)
            if "Materials" in xls.sheet_names
            else []
        )

        electricity_impacts = (
            parse_electricity_impacts(xls)
            if "Electricity" in xls.sheet_names
            else []
        )

        return ParsedBW2Workbook(
            activities=activities,
            material_impacts=material_impacts,
            electricity_impacts=electricity_impacts,
        )

def parse_activities_sheet(xls: pd.ExcelFile) -> List[ParsedActivity]:
    """
    Parse the matrix-style BW database sheet into
    flattened activity + exchange objects.
    """

    df = pd.read_excel(
        xls,
        sheet_name="BW database",
        header=None,
    )

    rows = df.values.tolist()

    activities: List[ParsedActivity] = []

    i = 0

    while i < len(rows):
        row = rows[i]

        first_cell = row[0]

        if first_cell == "Activity":
            activity_name = row[1]

            exchanges: List[ParsedExchange] = []

            # find exchanges section
            i += 1

            while i < len(rows):
                current_row = rows[i]

                if current_row[0] == "Exchanges":
                    break

                i += 1

            # skip:
            # Exchanges
            # header row
            i += 2

            while i < len(rows):
                exchange_row = rows[i]

                first_exchange_cell = exchange_row[0]

                # next activity block
                if first_exchange_cell == "Activity":
                    i -= 1
                    break

                # empty row
                if pd.isna(first_exchange_cell):
                    i += 1
                    continue

                exchange_name = exchange_row[0]
                amount = exchange_row[1]
                unit = exchange_row[2]

                # usually column 5 in BW2 exports
                exchange_type = exchange_row[4]

                # skip self-production exchange
                if exchange_type != "production":
                    exchanges.append(
                        ParsedExchange(
                            input_name=str(exchange_name),
                            amount=float(amount),
                            unit=None if pd.isna(unit) else str(unit),
                        )
                    )

                i += 1

            activities.append(
                ParsedActivity(
                    name=str(activity_name),
                    exchanges=exchanges,
                )
            )

        i += 1

    return activities


def parse_material_impacts(
    xls: pd.ExcelFile,
) -> List[ParsedMaterialImpact]:
    df = pd.read_excel(
        xls,
        sheet_name="Materials",
    )

    impacts: List[ParsedMaterialImpact] = []

    for _, row in df.iterrows():
        name = row.iloc[0]
        factor = row.iloc[1]

        if pd.isna(name):
            continue

        impacts.append(
            ParsedMaterialImpact(
                name=str(name),
                impact_factor=float(factor),
            )
        )

    return impacts


def parse_electricity_impacts(
    xls: pd.ExcelFile,
) -> List[ParsedElectricityImpact]:
    df = pd.read_excel(
        xls,
        sheet_name="Electricity",
    )

    impacts: List[ParsedElectricityImpact] = []

    for _, row in df.iterrows():
        name = row.iloc[0]
        factor = row.iloc[1]

        if pd.isna(name):
            continue

        impacts.append(
            ParsedElectricityImpact(
                name=str(name),
                impact_factor=float(factor),
            )
        )

    return impacts
