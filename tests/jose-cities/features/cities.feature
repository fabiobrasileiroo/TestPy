# Feature dos testes da API de Cities da FooAPI
# Feito por mim mesma pra organizar a bagunça :)

Feature: Testar a API de Cidades
  Aqui é só pra garantir que a desgrama da API tá rodando bonitinho e não vai quebrar no meio.

  Scenario: Listar cidades
    Given que eu quero ver todas as cidades
    When eu mando um GET /api/cities
    Then tem que voltar 200
    And tem que vir uma lista decente, não um trem vazio
    And cada cidade tem que ter type, properties e geometry certinho

  Scenario: Buscar cidade por ID
    Given que eu sei um ID válido (ou acho que sei)
    When eu mando GET /api/cities/{id}
    Then a API tem que me devolver 200
    And os dados da cidade certinho lá

  Scenario: ID zoado
    Given que eu invento um ID ridículo
    When eu mando GET /api/cities/abobrinha123
    Then a API TEM que reclamar
    And devolver 400 ou 404 pra eu saber que tá certo

  Scenario: Cidade aleatória
    Given que existe o endpoint rand
    When eu mando GET /api/cities/rand
    Then 200 tem que vir
    And a API tem que me mandar uma cidade aleatória qualquer

  Scenario: Criar cidade nova
    Given que eu monto um payload bonitinho
    When eu mando POST /api/cities
    Then tem que vir 200 ou 201
    And a API tem que devolver o ID novo
    And eu já salvo pra testar os updates depois

  Scenario: Atualizar tudo (PUT)
    Given que eu já tenho a cidade criada
    When eu faço PUT /api/cities/{id}
    Then a API tem que mandar 200
    And eu quero ver os dados atualizados lá direitinho

  Scenario: Atualizar só um campo (PATCH)
    Given que eu ainda tenho a cidade criada
    When eu faço PATCH /api/cities/{id}
    Then 200 na cara
    And só o campo que mudei tem que ter mudado, o resto fica quieto

  Scenario: Deletar cidade
    Given que eu tenho a cidade de testes lá
    When eu faço DELETE /api/cities/{id}
    Then tem que vir 200 ou 204
    And a cidade tem que sumir do mapa
