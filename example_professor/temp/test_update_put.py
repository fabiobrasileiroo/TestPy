import requests

BASE_URL = "https://jsonplaceholder.typicode.com/posts"


def test_update_post_put():
    """Atualizar um artigo completo"""
    artigo_atualizado = {
        "id": 1,
        "title": "Título Atualizado",
        "body": "Conteúdo completamente atualizado",
        "userId": 1
    }

    response = requests.put(f"{BASE_URL}/1", json=artigo_atualizado)

    print("PUT Atualizar Artigo:")
    print(f"Status: {response.status_code}")
    print(f"Título após update: {response.json()['title']}")
    print(f"Corpo após update: {response.json()['body'][:30]}...")
    print("-" * 50)


if __name__ == "__main__":
    test_update_post_put()
