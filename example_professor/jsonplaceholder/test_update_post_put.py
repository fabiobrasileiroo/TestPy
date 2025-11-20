import requests

def test_update_post_put():
    post_id = 1
    url = f'https://jsonplaceholder.typicode.com/posts/{post_id}'
    payload = {
        "id": post_id,
        "title": "Título Atualizado",
        "body": "Texto substituído completamente",
        "userId": 1
    }

    resposta = requests.put(url, json=payload)
    atualizado = resposta.json()

    assert resposta.status_code == 200
    assert atualizado['title'] == "Título Atualizado"
    assert atualizado['body'] == "Texto substituído completamente"
