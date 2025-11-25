Feature: comments API - Guilherme

  Verifica as operações de listar, consultar, criar, atualizar e excluir comentários
  utilizando o endpoint /comments da FooAPI.

  Background:
    Given que a url base da API é "https://fooapi.com"
    And que o endpoint para comments é "/comments"

  # ======================================================
  # GET /comments  (Listar todos)
  # ======================================================
  Scenario: Listar todos os comentários
    When eu enviar uma requisição GET para "/comments"
    Then o código de status da resposta deve ser 200
    And a resposta deve ser um array de JSON
    And o array deve conter pelo menos 1 elemento
    And cada comentário deve ter os campos "id, post_id, name, email e body"

  # ======================================================
  # GET /comments/{id}  (Buscar por ID)
  # ======================================================
  Scenario: Buscar um comentário específico por ID
    Given que existe um comentário com id "123"
    And que o comentário "123" está configurado na base de dados
    When eu enviar uma requisição GET para "/comments/123"
    Then o código de status da resposta deve ser 200
    And a resposta deve ser um objeto JSON
    And o objeto deve ser igual ao seguinte:
      | campo   | valor                        |
      | id      | 123                          |
      | post_id | 1                            |
      | name    | "Test User"                  |
      | email   | "test@example.com"           |
      | body    | "Este é um comentário para testes automáticos" |

  # ======================================================
  # POST /comments
  # ======================================================
  Scenario: Criar um novo comentário
    When eu enviar uma requisição POST para "/comments" com o seguinte corpo:
      """
      id="FOO-CMT"
      """
    Then o código de status da resposta deve ser 201
    And a resposta deve ser um objeto JSON

  # ======================================================
  # PUT /comments/{id}
  # ======================================================
  Scenario: Atualizar completamente um comentário via PUT
    Given que existe um comentário com id "789"
    And que o comentário "789" está configurado na base de dados
    When eu enviar uma requisição PUT para "/comments/789" com o seguinte corpo:
      """
      update
      """
    Then o código de status da resposta deve ser 200
    And a resposta deve ser um objeto JSON

  # ======================================================
  # PATCH /comments/{id}
  # ======================================================
  Scenario: Atualizar parcialmente um comentário via PATCH
    Given que existe um comentário com id "456"
    And que o comentário "456" está configurado na base de dados
    When eu enviar uma requisição PATCH para "/comments/456" com o seguinte corpo:
      """
      patch
      """
    Then o código de status da resposta deve ser 200
    And a resposta deve ser um objeto JSON

  # ======================================================
  # DELETE /comments/{id}
  # ======================================================
  Scenario: Excluir um comentário por ID
    Given que existe um comentário com id "999"
    And que o comentário "999" está configurado na base de dados
    When eu enviar uma requisição DELETE para "/comments/999"
    Then o código de status da resposta deve ser 200