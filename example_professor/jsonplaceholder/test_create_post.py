import requests

def test_create_post():
    url = 'https://jsonplaceholder.typicode.com/posts'
    payload = {
        "title": "Novo Post",
        "body": "Conteúdo do post criado via teste PyTest",
        "userId": 1
    }

    resposta = requests.post(url, json=payload)
    novo_post = resposta.json()

    assert resposta.status_code == 201
    assert novo_post['title'] == payload['title']
    assert 'id' in novo_post
