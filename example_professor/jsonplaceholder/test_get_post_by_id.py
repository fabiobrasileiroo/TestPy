import requests

def test_get_post_by_id():
    post_id = 1
    url = f'https://jsonplaceholder.typicode.com/posts/{post_id}'
    resposta = requests.get(url)

    assert resposta.status_code == 200
    post = resposta.json()
    assert post['id'] == post_id
    assert 'title' in post
