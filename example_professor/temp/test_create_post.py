import requests

BASE_URL = "https://jsonplaceholder.typicode.com/posts"


def test_create_post():
    """Criar um novo artigo"""
    novo_artigo = {
        "title": "Meu Novo Artigo",
        "body": "Conteúdo do meu artigo de teste",
        "userId": 1
    }

    response = requests.post(BASE_URL, json=novo_artigo)

    print("POST Criar Artigo:")
    print(f"Status: {response.status_code}")
    print(f"ID do novo artigo: {response.json()['id']}")
    print(f"Título: {response.json()['title']}")
    print(f"Corpo: {response.json()['body'][:30]}...")
    print(f"Autor: {response.json()['userId']}")
    print("-" * 50)


if __name__ == "__main__":
    test_create_post()
