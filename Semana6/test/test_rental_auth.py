class TestRentalAuth:
    """Tests de autenticación y autorización para Rent a Car"""

    def test_register_rental_user(self, client):
        data = {
            "username": "cliente_rental",
            "password": "123456",
            "role": "cliente_rental"
        }
        response = client.post("/auth/register", json=data)
        assert response.status_code == 201

    def test_login_rental_user(self, client):
        client.post("/auth/register", json={
            "username": "empleado_rental",
            "password": "empleado123",
            "role": "empleado_rental"
        })
        response = client.post("/auth/login", data={
            "username": "empleado_rental",
            "password": "empleado123"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()

    def test_create_alquiler_requires_auth(self, client, sample_alquiler_data):
        response = client.post("/rental_alquilers/", json=sample_alquiler_data)
        assert response.status_code == 401

    def test_admin_can_delete_alquiler(self, client, sample_alquiler_data, auth_headers):
        create_response = client.post("/rental_alquilers/", json=sample_alquiler_data, headers=auth_headers)
        alquiler_id = create_response.json()["id"]

        delete_response = client.delete(f"/rental_alquilers/{alquiler_id}", headers=auth_headers)
        assert delete_response.status_code == 200

    def test_regular_user_cannot_delete_alquiler(self, client, sample_alquiler_data):
        client.post("/auth/register", json={
            "username": "cliente_test",
            "password": "123456",
            "role": "cliente_rental"
        })
        login = client.post("/auth/login", data={
            "username": "cliente_test",
            "password": "123456"
        })
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        create_response = client.post("/rental_alquilers/", json=sample_alquiler_data, headers=headers)
        alquiler_id = create_response.json()["id"]

        delete_response = client.delete(f"/rental_alquilers/{alquiler_id}", headers=headers)
        assert delete_response.status_code == 403
