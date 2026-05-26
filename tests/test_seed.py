def test_list_activities(client):

    response = client.get("/activities")

    assert response.status_code == 200

    data = response.json()

    # --------------------------------------------------------
    # Validate seeded activities exist
    # --------------------------------------------------------

    assert data["count"] > 0

    assert len(data["activities"]) > 0

    # --------------------------------------------------------
    # Validate expected Company A activity exists
    # --------------------------------------------------------

    activity_names = [
        activity["name"]
        for activity in data["activities"]
    ]

    assert "Basic Biscuit Dough" in activity_names

    # --------------------------------------------------------
    # Validate exchange structure exists
    # --------------------------------------------------------

    first_activity = data["activities"][0]

    assert "exchanges" in first_activity

    assert isinstance(first_activity["exchanges"], list)