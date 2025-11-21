# language: pt
Funcionalidade: Movies API

  Contexto:
    URL base da API:"https://fooapi.com/docs/movies"
    Endpoint dos filmes:"https://fooapi.com/api/movies"

  # 1. Listar filmes – GET /api/movies
  Cenário: Listar todos os filmes
    Enviar uma requisição `GET` para "https://fooapi.com/api/movies"
    O código de status da resposta deve ser 200
    O array não pode estar zerado
    Cada filme deve ter os campos "id", "title", "year", "rated", "released", "runtime", "genre", "director", "writer", "actors", "plot", "language", "country", "awards", "poster", "imdbRating", "imdbId", "boxOffice"
   