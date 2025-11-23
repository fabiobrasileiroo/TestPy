# language: pt
Funcionalidade: Movies API

Cenário: Alterar um filme existente
    Dado o endpoint: "https://fooapi.com/api/movies/1"
    Quando eu enviar "https://fooapi.com/api/movies/1" alterando o título do filme:
    Então o novo nome do título deve ser: The lord of the rings