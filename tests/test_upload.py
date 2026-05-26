def test_partner_upload(client):

    with open(
        "app/data/Company_B_request.xlsx",
        "rb"
    ) as f:

        response = client.post(
            "/partner-recipes/upload",
            params={
                "partner_id": "Company B"
            },
            files={
                "file": (
                    "Company_B_request.xlsx",
                    f,
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            }
        )

    assert response.status_code == 200