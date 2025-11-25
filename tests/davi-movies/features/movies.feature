# language: pt
Funcionalidade: Movies API - Davi
  Como usuário da API de filmes
  Quero realizar operações de CRUD
  Para garantir que os endpoints funcionam corretamente

  Cenário: Listar todos os filmes
    Dado o endpoint: "https://fooapi.com/api/movies"
    Quando realizar a requisição GET no: "https://fooapi.com/api/movies"
    Então o código de status da resposta deve ser 200
    E cada filme deve ter os campos "title", "year", "rated", "released", "runtime", "genre", "director", "writer","actors", "plot", "language", "country", "awards", "poster", "imdbRating", "imdbId", "boxOffice"

  Cenário: Alterar um filme existente
    Dado o endpoint: "https://fooapi.com/api/movies/1"
    Quando eu enviar "https://fooapi.com/api/movies/1" alterando o título do filme:
    Então o código de status da resposta deve ser 201


  Cenário: Alterar um filme sem incluir campos obrigatórios
    Dado o endpoint: "https://fooapi.com/api/movies/1"
    Quando eu enviar "https://fooapi.com/api/movies/1" não incluindo campos obrigatórios
    Então o código de status da resposta deve ser 400

  Cenário: Criar um novo filme
    Dado o endpoint: "https://fooapi.com/api/movies"
    Quando eu realizar a requisição POST no endpoint: "https://fooapi.com/api/movies"
    Então o código de status da resposta deve ser 201

  Cenário: Deletar um filme
    Dado o endpoint: "https://fooapi.com/api/movies/3"
    Quando eu realizar a requisição DELETE no endpoint: "https://fooapi.com/api/movies/3"
    Então o código de status da resposta deve ser 200
