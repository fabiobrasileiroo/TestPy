

import pytest
from .utils_cities import (
    get_all_cities, get_city_by_id, get_random_city,
    create_city, update_city, patch_city, delete_city
)
from .fixtures_cities import (
    new_city_payload, updated_city_payload, partial_update_payload
)

def test_get_all_cities():
    resp = get_all_cities()
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    # opcional: verificar que cada item é um Feature GeoJSON
    for item in data:
        assert "type" in item and item["type"] == "Feature"
        assert "properties" in item
        assert "geometry" in item

def test_get_city_by_invalid_id():
    resp = get_city_by_id("invalid-id-123")
    # dependendo da API, pode retornar 404 ou outro erro
    assert resp.status_code in (400, 404)

def test_get_random_city():
    resp = get_random_city()
    assert resp.status_code == 200
    city = resp.json()
    assert "type" in city and city["type"] == "Feature"
    assert "properties" in city and "name" in city["properties"]

@pytest.mark.order(1)
def test_create_city_and_then_delete():
    # Cria a cidade
    resp = create_city(new_city_payload)
    assert resp.status_code == 201 or resp.status_code == 200
    city = resp.json()
    # Verifica estrutura
    assert city["properties"]["name"] == new_city_payload["properties"]["name"]
    assert "id" in city or "_id" in city  # depende como a API retorna o identificador

    # Captura o id
    city_id = city.get("id") or city.get("_id")
    assert city_id is not None

    # Deleta a cidade
    resp_del = delete_city(city_id)
    assert resp_del.status_code in (200, 204)

@pytest.mark.order(2)
def test_update_city():
    # Primeiro, cria a cidade para testar update
    resp = create_city(new_city_payload)
    assert resp.status_code in (200, 201)
    city = resp.json()
    city_id = city.get("id") or city.get("_id")

    # Atualiza completamente
    resp_put = update_city(city_id, updated_city_payload)
    assert resp_put.status_code == 200
    updated = resp_put.json()
    assert updated["properties"]["name"] == updated_city_payload["properties"]["name"]
    assert updated["properties"]["population"] == updated_city_payload["properties"]["population"]

    # Deleta no final
    delete_city(city_id)

@pytest.mark.order(3)
def test_patch_city():
    # Cria a cidade de teste
    resp = create_city(new_city_payload)
    city = resp.json()
    city_id = city.get("id") or city.get("_id")

    # Atualiza parcialmente
    resp_patch = patch_city(city_id, partial_update_payload)
    assert resp_patch.status_code == 200
    patched = resp_patch.json()
    assert patched["properties"]["population"] == partial_update_payload["properties"]["population"]

    # Deleta no final
    delete_city(city_id)

