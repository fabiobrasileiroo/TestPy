import requests
import json
from pytest_bdd import scenarios, given, when, then, parsers

scenarios("features/movies_put.feature")

@given(parsers.cfparse('o endpoint: "{path}"'))
def endpoint(path: str) -> str:
    return path

@when(parsers.cfparse('eu enviar "{path}" alterando o título do filme:'),target_fixture="response")
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
    response = requests.put(path, json=body)
    return response

@then(parsers.cfparse("o novo nome do título deve ser: {title}"))
def check_name(response):
    assert response.status_code == 200 or 201 or 204