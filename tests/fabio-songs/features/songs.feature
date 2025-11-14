# language: pt
Funcionalidade: Songs API

  # 1. Listar músicas – GET /api/songs
  Contexto:
    Dado que a url base da API é "https://fooapi.com"
    E que o endpoint para listar músicas é "/api/songs"

  Cenário: Listar todas as músicas
    Quando eu enviar uma requisição `GET` para "/api/songs"
    Então o código de status da resposta deve ser 200
    E a resposta deve ser um array de `JSON`
    E o array deve conter pelo menos 1 música
    E cada música deve ter os campos "id", "name", "artists", "isExplicit", "durationMs", "albumName" e "albumReleaseDate"
  