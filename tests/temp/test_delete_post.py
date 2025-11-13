import requests

BASE_URL = "https://jsonplaceholder.typicode.com/posts"


def test_delete_post():
    """Excluir um artigo"""
    response = requests.delete(f"{BASE_URL}/1")

    print("DELETE Excluir Artigo:")
    print(f"Status: {response.status_code}")
    print(f"Resposta: {response.json()}")
    print("Artigo excluído com sucesso!")
    print("-" * 50)


if __name__ == "__main__":
    test_delete_post()