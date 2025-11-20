import requests

def test_partial_update_post_patch():
    post_id = 1
    url = f'https://jsonplaceholder.typicode.com/posts/{post_id}'
    payload = {"title": "Título Parcialmente Atualizado"}

    resposta = requests.patch(url, json=payload)
    atualizado = resposta.json()

    assert resposta.status_code == 200
    assert atualizado['title'] == "Título Parcialmente Atualizado"
