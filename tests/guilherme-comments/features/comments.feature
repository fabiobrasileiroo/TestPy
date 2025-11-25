Feature: comments API - Guilherme

  Verifica as operações de listar, consultar, criar, atualizar e excluir comentários
  utilizando o endpoint /api/comments da FooAPI.

  Background:
    Given que a url base da API é "https://fooapi.com"
    And que o endpoint para comments é "/api/comments"

  # ======================================================
  # GET /api/comments  (Listar todos)
  # ======================================================
  Scenario: Listar todos os comentários
    When eu enviar uma requisição GET para "/api/comments"
    Then o código de status da resposta deve ser 200
    And a resposta deve ser um array de JSON
    And o array deve conter pelo menos 1 elemento
    And cada comentário deve ter os campos "id, postId, comment e user.name"

  # ======================================================
  # GET /api/comments/{id}  (Buscar por ID)
  # ======================================================
  Scenario: Buscar um comentário específico por ID
    Given que existe um comentário com id "1"
    And que o comentário "1" está configurado na base de dados
    When eu enviar uma requisição GET para "/api/comments/1"
    Then o código de status da resposta deve ser 200
    And a resposta deve ser um objeto JSON
    And o objeto deve ter os campos "id, postId, comment e user"

  # ======================================================
  # POST /api/comments
  # ======================================================
  Scenario: Criar um novo comentário
    When eu enviar uma requisição POST para "/api/comments" com o seguinte corpo:
      """
      id="FOO-CMT"
      """
    Then o código de status da resposta deve ser 201
    And a resposta deve ser um objeto JSON

  # ======================================================
  # PUT /api/comments/{id}
  # ======================================================
  Scenario: Atualizar completamente um comentário via PUT
    Given que existe um comentário com id "1"
    And que o comentário "1" está configurado na base de dados
    When eu enviar uma requisição PUT para "/api/comments/1" com o seguinte corpo:
      """
      update
      """
    Then o código de status da resposta deve ser 201
    And a resposta deve ser um objeto JSON

  # ======================================================
  # PATCH /api/comments/{id}
  # ======================================================
  Scenario: Atualizar parcialmente um comentário via PATCH
    Given que existe um comentário com id "1"
    And que o comentário "1" está configurado na base de dados
    When eu enviar uma requisição PATCH para "/api/comments/1" com o seguinte corpo:
      """
      patch
      """
    Then o código de status da resposta deve ser 201
    And a resposta deve ser um objeto JSON

  # ======================================================
  # DELETE /api/comments/{id}
  # ======================================================
  Scenario: Excluir um comentário por ID
    Given que existe um comentário com id "1"
    And que o comentário "1" está configurado na base de dados
    When eu enviar uma requisição DELETE para "/api/comments/1"
    Then o código de status da resposta deve ser 200
