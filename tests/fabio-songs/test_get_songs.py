import json
import requests
from pytest_bdd import scenarios, given, when, then, parsers

# use centralized config for env variables
from app.config import BASE_URL


scenarios("features/songs.feature")


@given(parsers.cfparse('que a url base da API é "{base_url}"'))
def base_url(base_url):
    return base_url


@when(parsers.cfparse('eu enviar uma requisição `GET` para "{path}"'))
def send_get_request(base_url, path):
    url = base_url + path
    resp = requests.get(url)
    return resp


@then(parsers.cfparse('o código de status da resposta deve ser {status_code:d}'))
def check_status_code(response, status_code):
    assert response.status_code == status_code


@then('a resposta deve ser um array de `JSON`')
def check_json_array(response):
    data = response.json()
    assert isinstance(data, list)


@then('o array deve conter pelo menos 1 música')
def check_array_not_empty(response):
    data = response.json()
    assert len(data) >= 1


@then(parsers.cfparse('cada música deve ter os campos "{fields}"'))
def check_song_fields(response, fields):
    expected_fields = [f.strip().strip('"') for f in fields.split(',')]
    data = response.json()
    assert isinstance(data, list) and data
    for song in data:
        for f in expected_fields:
            assert f in song
import json
import requests
from pytest_bdd import scenarios, given, when, then, parsers

# environment variables
from dotenv import load_dotenv
import os
load_dotenv()  # carrega variáveis do .env
BASE_URL = os.getenv("BASE_URL", "http://fooapi.com")


scenarios("features/songs.feature")


@given(parsers.cfparse('que a url base da API é "{base_url}"'))
def base_url(base_url):
  return base_url


@when(parsers.cfparse('eu enviar uma requisição `GET` para "{path}"'))
def send_get_request(base_url, path):
  url = base_url + path
  resp = requests.get(url)
  return resp


@then(parsers.cfparse('o código de status da resposta deve ser {status_code:d}'))
def check_status_code(response, status_code):
  assert response.status_code == status_code


@then('a resposta deve ser um array de `JSON`')
def check_json_array(response):
  data = response.json()
  assert isinstance(data, list)


@then('o array deve conter pelo menos 1 música')
def check_array_not_empty(response):
  data = response.json()
  assert len(data) >= 1


@then(parsers.cfparse('cada música deve ter os campos "{fields}"'))
def check_song_fields(response, fields):
  expected_fields = [f.strip().strip('"') for f in fields.split(',')]
  data = response.json()
  assert isinstance(data, list) and data
  for song in data:
    for f in expected_fields:
      assert f in song

