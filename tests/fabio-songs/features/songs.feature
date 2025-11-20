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
    E a resposta deve conter a seguinte música com um array de objetos com os seguintes valores:
      | campo             | valor               |
      | id                | 1                   |
      | name              | Espresso            |
      | artists           | "Sabrina Carpenter" |
      | isExplicit        | true                |
      | durationMs        | 175459              |
      | albumName         | Espresso            |
      | albumReleaseDate  | 2024-04-12          |

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
    # Quando eu enviar a data do "albumReleaseDate" e for maior que a data atual
    # Então deve retornar um erro com status 400 informando que o valor maior que data atual não permitido

  # 3. Atualizar música – PUT /api/songs/{id}
  Cenário: Atualizar música com um id existente
    Dado que existe uma música com id "1"
    Quando eu enviar uma requisição `PUT` para "/api/songs/1" com o seguinte corpo:
      """ json
      {
        "name": "New Espresso",
        "artists": "New Artist", // está no plural, mas apenas uma string é esperada e não um array
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
      | artists           | "New Artist"        |
      | isExplicit        | false               |
      | durationMs        | 180000              |
      | albumName         | New espresso        |
      | albumReleaseDate  | 2025-01-01          |
  
  # 4.Criar música - POST /api/songs
  Cenário: Criar uma nova música
    Quando eu enviar uma requisição `POST` para "/api/songs" com o seguinte corpo:
      """ json
      {
        "name": "foooName",
        "artists": "fooArtist",
        "isExplicit": true,
        "durationMs": 175459,
        "albumName": "FooAlbum",
        "albumReleaseDate": "2024-04-12"
      }
      """
    Então o código de status da resposta deve ser 201
    E a resposta deve ser um objeto `JSON`
    E o objeto deve ter os campos "id", "name", "artists", "isExplicit", "durationMs", "albumName" e "albumReleaseDate"
    E a resposta deve ser um objeto com os seguintes valores:
      | campo             | valor               |
      | id                | "fooArtist"         |
      | name              | "foooName"          |
      | artists           | "fooArtist"         |
      | isExplicit        | true                |
      | durationMs        | 175459              |
      | albumName         | "FooAlbum"          |
      | albumReleaseDate  | "2024-04-12"        |


  # 5. Deletar música - DELETE /api/songs/{id}
  Cenário: Deletar música com um id existente
    Dado que existe uma música com id "1"
    Quando eu enviar uma requisição `DELETE` para "/api/songs/1"
    Então o código de status da resposta deve ser 204
    E a resposta deve ser um objeto com os seguinte valor:
      | campo   | valor |
      | id      | "1"   |

