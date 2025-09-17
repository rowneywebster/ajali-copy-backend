def test_signup(client):
    response = client.post("/api/v1/auth/signup", json={"email": "test@example.com", "password": "123"})
    assert response.status_code == 201
    assert "User registered" in response.get_json()["message"]
