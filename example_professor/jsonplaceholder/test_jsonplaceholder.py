import requests

BASE_URL = "https://jsonplaceholder.typicode.com/posts"


def test_get_posts():
    """Teste simples de GET em /posts"""
    resposta = requests.get(BASE_URL)
    assert resposta.status_code == 200
    dados = resposta.json()
    assert isinstance(dados, list)
    assert 'userId' in dados[0]


def test_get_post_by_id():
    """Teste de GET em /posts/{id}"""
    post_id = 1
    resposta = requests.get(f"{BASE_URL}/{post_id}")
    assert resposta.status_code == 200
    post = resposta.json()
    assert post['id'] == post_id
    assert 'title' in post


def test_create_post():
    """Teste de POST (criação de post)"""
    payload = {
        "title": "Novo Post",
        "body": "Conteúdo criado via PyTest",
        "userId": 1
    }

    resposta = requests.post(BASE_URL, json=payload)
    assert resposta.status_code == 201
    novo_post = resposta.json()
    assert novo_post['title'] == payload['title']
    assert 'id' in novo_post


def test_update_post_put():
    """Teste de PUT (atualização completa do post)"""
    post_id = 1
    payload = {
        "id": post_id,
        "title": "Título Atualizado",
        "body": "Texto substituído completamente",
        "userId": 1
    }

    resposta = requests.put(f"{BASE_URL}/{post_id}", json=payload)
    assert resposta.status_code == 200
    atualizado = resposta.json()
    assert atualizado['title'] == "Título Atualizado"
    assert atualizado['body'] == "Texto substituído completamente"


def test_partial_update_post_patch():
    """Teste de PATCH (atualização parcial do post)"""
    post_id = 1
    payload = {"title": "Título Parcialmente Atualizado"}

    resposta = requests.patch(f"{BASE_URL}/{post_id}", json=payload)
    assert resposta.status_code == 200
    atualizado = resposta.json()
    assert atualizado['title'] == "Título Parcialmente Atualizado"


def test_delete_post():
    """Teste de DELETE (remoção de post)"""
    post_id = 1
    headers = {'Accept': '*/*', 'User-Agent': 'pytest-client'}

    resposta = requests.delete(f"{BASE_URL}/{post_id}", headers=headers)
    assert resposta.status_code == 200
