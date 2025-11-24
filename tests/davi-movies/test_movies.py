import requests
import json
from pytest_bdd import scenarios, given, when, then, parsers

# Carrega o arquivo de feature único
scenarios("features/movies.feature")


# Step comum: Dado o endpoint
@given(parsers.cfparse('o endpoint: "{path}"'))
def endpoint(path: str) -> str:
    return path


# Função auxiliar para extrair dados da resposta
def extract_datas(response):
    data = response.json()
    if isinstance(data, dict) and "data" in data and isinstance(data["data"], list):
        return data["data"]
    return data

# ============================================================
# Caso 1: Listar todos os filmes (GET)
# ============================================================
@when(parsers.cfparse('realizar a requisição GET no: "{path}"'),
      target_fixture="response")
def request_api(path: str):
    response = requests.get(path)
    return response

@then(parsers.cfparse('o código de status da resposta deve ser {status_code:d}'))
def check_status_code(response, status_code):
    assert response.status_code == status_code

@then(parsers.cfparse('cada filme deve ter os campos "{fields}"'))
def check_movie_labels(response, fields):
    # separa os campos por vírgula
    expected_labels = [f.strip().strip('"') for f in fields.split(',') if f.strip()]
    data = extract_datas(response)
    assert isinstance(data, list) and data
    for movie in data:
        for f in expected_labels:
            assert f in movie


# Caso 2: Alterar um filme existente (PUT com título)
@when(parsers.cfparse('eu enviar "{path}" alterando o título do filme:'), target_fixture="response")
def send_put_request(path: str):
    body = {
        "id": "1",
        "title": "The lord of the rings",
        "year": "1994",
        "rated": "R",
        "released": "14-10-1994",
        "runtime": "142 min",
        "genre": "Drama",
        "director": "Frank Darabont",
        "writer": "Stephen King, Frank Darabont",
        "actors": "Tim Robbins, Morgan Freeman, Bob Gunton",
        "plot": "Over the course of several years...",
        "language": "English",
        "country": "United States",
        "awards": "Nominated for 7 Oscars. 21 wins & 42 nominations total",
        "poster": "https://m.media-amazon.com/images/...",
        "imdbRating": "9.3",
        "imdbId": "tt0111161",
        "boxOffice": "$28,767,189"
    }
    return requests.put(path, json=body)

@then(parsers.cfparse("o código de status da resposta deve ser {status_code:d}"))
def check_put_status(response, status_code):
    assert response.status_code == status_code


# Caso 3: Alterar um filme sem incluir campos obrigatórios (PUT inválido)
@when(parsers.cfparse('eu enviar "{path}" não incluindo campos obrigatórios'), target_fixture="response")
def send_put_request_invalid(path: str):
    body = {
        "id": "1",
        "year": "1994",
        "rated": "R",
        "released": "14-10-1994",
        "director": "Frank Darabont",
        "writer": "Stephen King, Frank Darabont",
        "actors": "Tim Robbins, Morgan Freeman, Bob Gunton",
        "plot": "Over the course of several years...",
        "language": "English",
        "country": "United States",
        "awards": "Nominated for 7 Oscars. 21 wins & 42 nominations total",
        "poster": "https://m.media-amazon.com/images/...",
        "imdbRating": "9.3",
        "imdbId": "tt0111161",
        "boxOffice": "$28,767,189"
    }
    return requests.put(path, json=body)

@then(parsers.cfparse("o código de status da resposta deve ser {status_code:d}"))
def check_put_invalid(response, status_code):
    assert response.status_code == status_code

# Caso 4: Criar um novo filme (POST)
@when(parsers.cfparse('eu realizar a requisição POST no endpoint: "{path}"'), target_fixture="response")
def send_post_request(path: str):
    body = {
        "title": "The lord of the rings",
        "year": "1994",
        "rated": "R",
        "released": "14-10-1994",
        "runtime": "142 min",
        "genre": "Drama",
        "director": "Frank Darabont",
        "writer": "Stephen King, Frank Darabont",
        "actors": "Tim Robbins, Morgan Freeman, Bob Gunton",
        "plot": "Over the course of several years...",
        "language": "English",
        "country": "United States",
        "awards": "Nominated for 7 Oscars. 21 wins & 42 nominations total",
        "poster": "https://m.media-amazon.com/images/...",
        "imdbRating": "9.3",
        "imdbId": "tt0111161",
        "boxOffice": "$28,767,189"
    }
    return requests.post(path, json=body)

@then(parsers.cfparse('o código de status da resposta deve ser {status_code:d}'))
def check_post_status(response, status_code):
    assert response.status_code == status_code

@then("o novo filme deve conter um ID que seja maior que 0")
def check_id_not_zero(response):
    data = response.json()
    assert "data" in data, f"Resposta não contém 'data': {data}"
    movie = data["data"]
    assert "id" in movie, f"Resposta não contém 'id': {movie}"
    id_value = int(movie["id"])
    assert id_value > 0, f"O id retornado é inválido: {id_value}"


# Caso 5: Deletar um filme (DELETE)
@when(parsers.cfparse('eu realizar a requisição DELETE no endpoint: "{path}"'), target_fixture="response")
def send_delete_request(path: str):
    return requests.delete(path)

@then(parsers.cfparse('o código de status da resposta deve ser {status_code:d}'))
def check_delete_status(response, status_code):
    assert response.status_code == status_code
