def test_list_incidents(client):
    response = client.get("/api/v1/incidents/")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
