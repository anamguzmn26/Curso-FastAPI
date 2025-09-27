import pytest
from fastapi import status

@pytest.mark.tipo_c
def test_crud_completo_usuario(authenticated_client, sample_user_generic):
    # CREATE
    resp_create = authenticated_client.post("/usuarios/", json=sample_user_generic)
    assert resp_create.status_code == status.HTTP_200_OK or resp_create.status_code == status.HTTP_201_CREATED
    usuario_id = resp_create.json()["id"]

    # READ
    resp_get = authenticated_client.get(f"/usuarios/{usuario_id}")
    assert resp_get.status_code == status.HTTP_200_OK
    assert resp_get.json()["nombre"] == sample_user_generic["nombre"]

    # UPDATE
    resp_update = authenticated_client.put(f"/usuarios/{usuario_id}", json={"nombre": "Nuevo Nombre"})
    assert resp_update.status_code == status.HTTP_200_OK
    assert resp_update.json()["nombre"] == "Nuevo Nombre"

    # DELETE
    resp_delete = authenticated_client.delete(f"/usuarios/{usuario_id}")
    assert resp_delete.status_code == status.HTTP_204_NO_CONTENT

    # READ NOT FOUND
    resp_get2 = authenticated_client.get(f"/usuarios/{usuario_id}")
    assert resp_get2.status_code == status.HTTP_404_NOT_FOUND
