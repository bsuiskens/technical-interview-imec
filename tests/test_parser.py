from app.bw_parser import parse_bw2_workbook


def test_parse_company_a_workbook():

    parsed = parse_bw2_workbook(
        "app/data/Company_A_Database.xlsx"
    )

    assert len(parsed.activities) > 0

    names = [a.name for a in parsed.activities]

    assert "Basic Biscuit Dough" in names