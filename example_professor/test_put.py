import requests

def test_put_new_data():
    headers = {
        'Accept': '*/*',
        'User-Agent': 'request'
    }

    new_data = {
        "id": 1,
        "title": "A test title",
        "body": "Some test description",
        "userId": '1'
    }

    post_id = 1

    url = 'https://jsonplaceholder.typicode.com/posts/'

    resposta = requests.put(url + str(post_id), data=new_data, headers=headers)
    resposta_dict = resposta.json()

    if resposta.status_code == 200:
        assert resposta_dict == new_data
    else:
        assert False