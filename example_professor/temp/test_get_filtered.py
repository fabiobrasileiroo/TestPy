import requests

BASE_URL = "https://jsonplaceholder.typicode.com/posts"


def test_get_posts_by_user():
    """Buscar artigos de um usuário específico"""
    response = requests.get(f"{BASE_URL}?userId=1")

    print("GET Artigos por Usuário:")
    print(f"Status: {response.status_code}")
    print(f"Quantidade de artigos do usuário 1: {len(response.json())}")

    for i, post in enumerate(response.json()[:3]):  # Mostra apenas 3
        print(f"  {i + 1}. {post['title'][:40]}...")
    print("-" * 50)


if __name__ == "__main__":
    test_get_posts_by_user()