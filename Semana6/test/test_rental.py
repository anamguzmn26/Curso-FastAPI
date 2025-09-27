import pytest

class TestRentalAPI:
    """Tests CRUD y validaciones para Rent a Car"""

    def test_create_alquiler_success(self, client, sample_alquiler_data, auth_headers):
        response = client.post("/rental_alquilers/", json=sample_alquiler_data, headers=auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["cliente"] == sample_alquiler_data["cliente"]
        assert data["vehiculo"] == sample_alquiler_data["vehiculo"]

    def test_create_alquiler_invalid_age(self, client, auth_headers):
        invalid_data = {
            "cliente": "Pedro Niño",
            "vehiculo": "Chevrolet Spark",
            "fecha_inicio": "2025-10-01",
            "fecha_fin": "2025-10-03",
            "precio_diario": 80000,
            "licencia_valida": True,
            "edad_conductor": 17
        }
        response = client.post("/rental_alquilers/", json=invalid_data, headers=auth_headers)
        assert response.status_code == 422
        assert "edad mínima" in response.json()["detail"].lower()

    def test_get_alquiler_by_id(self, client, sample_alquiler_data, auth_headers):
        create_response = client.post("/rental_alquilers/", json=sample_alquiler_data, headers=auth_headers)
        alquiler_id = create_response.json()["id"]

        response = client.get(f"/rental_alquilers/{alquiler_id}", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["id"] == alquiler_id

    def test_update_alquiler(self, client, sample_alquiler_data, auth_headers):
        create_response = client.post("/rental_alquilers/", json=sample_alquiler_data, headers=auth_headers)
        alquiler_id = create_response.json()["id"]

        update_data = {**sample_alquiler_data, "precio_diario": 150000}
        response = client.put(f"/rental_alquilers/{alquiler_id}", json=update_data, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["precio_diario"] == 150000

    def test_delete_alquiler(self, client, sample_alquiler_data, auth_headers):
        create_response = client.post("/rental_alquilers/", json=sample_alquiler_data, headers=auth_headers)
        alquiler_id = create_response.json()["id"]

        delete_response = client.delete(f"/rental_alquilers/{alquiler_id}", headers=auth_headers)
        assert delete_response.status_code == 200

        get_response = client.get(f"/rental_alquilers/{alquiler_id}", headers=auth_headers)
        assert get_response.status_code == 404
