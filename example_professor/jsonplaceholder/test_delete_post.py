import requests

def test_delete_post():
    post_id = 1
    url = f'https://jsonplaceholder.typicode.com/posts/{post_id}'
    headers = {'Accept': '*/*', 'User-Agent': 'pytest-client'}

    resposta = requests.delete(url, headers=headers)
    assert resposta.status_code == 200
