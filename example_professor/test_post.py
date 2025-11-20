import requests
import pytest


def test_insert_employee():
    headers = {
        'Accept': '*/*',
        'User-Agent': 'request'
    }

    url = 'http://dummy.restapiexample.com/api/v1/create'

    new_employee = {'name': 'Testerson', 'salary': '5000', 'age': '32'}

    resposta = requests.post(url, headers=headers, data=new_employee)

    # Avoid calling .json() on non-JSON responses (e.g. 429 HTML responses).
    if resposta.status_code != 200:
        pytest.skip(f"External API returned status {resposta.status_code}; skipping")

    resposta_dict = resposta.json()

    status = resposta_dict.get('status')
    employee_response = resposta_dict.get('data')

    assert status == 'success' and employee_response and employee_response.get('id') is not None
