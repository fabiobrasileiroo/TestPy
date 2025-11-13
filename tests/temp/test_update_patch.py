import requests

BASE_URL = "https://jsonplaceholder.typicode.com/posts"


def test_update_post_patch():
    """Atualizar apenas parte do artigo"""
    atualizacao_parcial = {
        "title": "Apenas o título foi modificado"
    }

    response = requests.patch(f"{BASE_URL}/1", json=atualizacao_parcial)

    print("PATCH Atualizar Parcial:")
    print(f"Status: {response.status_code}")
    print(f"Novo título: {response.json()['title']}")
    print(f"Corpo (inalterado): {response.json()['body'][:30]}...")
    print("-" * 50)


if __name__ == "__main__":
    test_update_post_patch()
