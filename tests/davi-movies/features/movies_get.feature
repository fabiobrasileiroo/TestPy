# language: pt
Funcionalidade: Movies API

  Cenário: Listar todos os filmes
    Dado o endpoint: "https://fooapi.com/api/movies"
    Quando realizar a requisição GET no: "https://fooapi.com/api/movies"
    Então o código de status da resposta deve ser 200
    E cada filme deve ter os campos "id", "title", "year", "rated", "released", "runtime", "genre", "director", "writer", "actors", "plot", "language", "country", "awards", "poster", "imdbRating", "imdbId", "boxOffice"
