def test_baked_biscuit_impact(client):

    response = client.get(
        "/activities/Baked Biscuit Wafers/impact"
    )

    assert response.status_code == 200

    data = response.json()
    # I don't actually don't have "known correct outcomes", so for the time being I can't confidently give a correct number. 
    assert data["total_impact"] > 0