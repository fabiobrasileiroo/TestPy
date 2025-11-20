import requests

BASE_URL = "https://jsonplaceholder.typicode.com/posts"


def test_get_all_posts():
    """Buscar todos os artigos"""
    response = requests.get(BASE_URL)

    print("GET Todos os Artigos:")
    print(f"Status: {response.status_code}")
    print(f"Quantidade: {len(response.json())} artigos")
    print(f"Primeiro artigo: {response.json()[0]['title'][:50]}...")
    print("-" * 50)


def test_get_single_post():
    """Buscar um artigo específico"""
    response = requests.get(f"{BASE_URL}/1")

    print("GET Artigo Específico:")
    print(f"Status: {response.status_code}")
    print(f"ID: {response.json()['id']}")
    print(f"Título: {response.json()['title']}")
    print(f"Autor (userId): {response.json()['userId']}")
    print("-" * 50)


if __name__ == "__main__":
    test_get_all_posts()
    test_get_single_post()