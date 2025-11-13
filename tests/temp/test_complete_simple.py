import requests

BASE_URL = "https://jsonplaceholder.typicode.com/posts"


def test_complete_crud():
    """Teste completo e simples de todas as operações"""

    # GET - Buscar
    print("1. BUSCANDO artigo 1...")
    response_get = requests.get(f"{BASE_URL}/1")
    print(f"   Título original: {response_get.json()['title']}")

    # POST - Criar
    print("2. CRIANDO novo artigo...")
    novo_artigo = {
        "title": "Artigo de Teste CRUD",
        "body": "Testando todas as operações",
        "userId": 1
    }
    response_post = requests.post(BASE_URL, json=novo_artigo)
    print(f"   Novo ID: {response_post.json()['id']}")

    # PUT - Atualizar
    print("3. ATUALIZANDO artigo 1...")
    artigo_atualizado = {
        "id": 1,
        "title": "Artigo ATUALIZADO",
        "body": "Conteúdo atualizado via PUT",
        "userId": 1
    }
    response_put = requests.put(f"{BASE_URL}/1", json=artigo_atualizado)
    print(f"   Novo título: {response_put.json()['title']}")

    # DELETE - Excluir
    print("4. EXCLUINDO artigo 1...")
    response_delete = requests.delete(f"{BASE_URL}/1")
    print(f"   Status: {response_delete.status_code}")

    print("-" * 50)
    print("CRUD completo executado com sucesso!")


if __name__ == "__main__":
    test_complete_crud()
