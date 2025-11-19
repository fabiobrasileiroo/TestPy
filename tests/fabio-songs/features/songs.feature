# language: pt
Funcionalidade: Songs API

  Contexto:
    Dado que a url base da API é "https://fooapi.com"
    E que o endpoint para listar músicas é "/api/songs"

  # 1. Listar músicas – GET /api/songs
  Cenário: Listar todas as músicas
    Quando eu enviar uma requisição `GET` para "/api/songs"
    Então o código de status da resposta deve ser 200
    E a resposta deve ser um array de `JSON`
    E o array deve conter pelo menos 1 música
    E cada música deve ter os campos "id", "name", "artists", "isExplicit", "durationMs", "albumName" e "albumReleaseDate"

  # 2. Listar música por ID – GET /api/songs/{id}
  Cenário: Listar música com um id existente
    Dado que existe uma música com id "1"
    Quando eu enviar uma requisição `GET` para "/api/songs/1"
    Então o código de status da resposta deve ser 200
    E a resposta deve ser um objeto `JSON`
    E o objeto deve ter os campos "id", "name", "artists", "isExplicit", "durationMs", "albumName" e "albumReleaseDate"
    E a resposta deve ser um objeto com os seguintes valores:
      | campo             | valor               |
      | id                | 1                   |
      | name              | Espresso            |
      | artists           | "Sabrina Carpenter" |
      | isExplicit        | true                |
      | durationMs        | 175459              |
      | albumName         | Espresso            |
      | albumReleaseDate  | 2024-04-12          |

  # 3. Atualizar música – PUT /api/songs/{id}
  Cenário: Atualizar música com um id existente
    Dado que existe uma música com id "1"
    Quando eu enviar uma requisição `PUT` para "/api/songs/1" com o seguinte corpo:
      """ json
      {
        "name": "New Espresso",
        "artists": ["New Artist"],
        "isExplicit": false,
        "durationMs": 180000,
        "albumName": "New espresso",
        "albumReleaseDate": "2025-01-01"
      }
      """
      Então o código de status da resposta deve ser 200
      E a resposta deve ser um objeto `JSON`
      E o objeto deve os campos "id", "name", "artists", "isExplicit", "durationMs", "albumName" e "albumReleaseDate"
      E a resposta deve ser um objeto com os seguintes valores:
        | campo             | valor               |
        | id                | 1                   |
        | name              | New Espresso        |
        | artists           | "New Artist"       |
        | isExplicit        | false               |
        | durationMs        | 180000              |
        | albumName         | New espresso        |
        | albumReleaseDate  | 2025-01-01          |
  
  # 4. Deletar música - DELETE /api/songs/{id}
  Cenário: Deletar música com um id existente
    Dado que existe uma música com id "1"
    Quando eu enviar uma requisição `DELETE` para "/api/songs/1"
    Então o código de status da resposta deve ser 204
    
