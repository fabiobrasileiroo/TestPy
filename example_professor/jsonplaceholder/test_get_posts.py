import requests

def test_get_posts():
    url = 'https://jsonplaceholder.typicode.com/posts'
    resposta = requests.get(url)

    assert resposta.status_code == 200
    dados = resposta.json()
    assert isinstance(dados, list)
    assert 'userId' in dados[0]
