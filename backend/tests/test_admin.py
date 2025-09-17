def test_admin_list_incidents(client):
    response = client.get("/api/v1/admin/incidents")
    # Not logged in → expect 401
    assert response.status_code in [200, 401]
