Feature: cidades API

  Scenario: 1. Criar uma nova cidade
    Given que a url base da API é "https://fooapi.com"
    And que o endpoint para cidades é "/api/cities"
    When eu enviar uma requisição `POST` para "/api/cities" com o seguinte corpo:
    Then o código de status da resposta deve ser 201
    And a resposta deve ser um objeto `JSON`
    And o objeto deve ser igual ao seguinte:
      | campo | valor |
      | id    | "FOO" |

  Scenario: 2. Listar todas as cidades
    Given que a url base da API é "https://fooapi.com"
    And que o endpoint para cidades é "/api/cities"
    When eu enviar uma requisição `GET` para "/api/cities"
    Then o código de status da resposta deve ser 200
    And a resposta deve ser um array de `JSON`

  Scenario: 3. Buscar cidade por ID
    Given que a url base da API é "https://fooapi.com"
    And que o endpoint para cidades é "/api/cities"
    And que a cidade "BD" é configurada na base de dados
    When eu enviar uma requisição `GET` para "/api/cities/BD"
    Then o código de status da resposta deve ser 200
    And a resposta deve ser um objeto `JSON`
    And o objeto deve ser igual ao seguinte:
      | campo | valor |
      | id    | "BD" |

  Scenario: 4. Atualizar uma cidade existente
    Given que a url base da API é "https://fooapi.com"
    And que o endpoint para cidades é "/api/cities"
    And que a cidade "BD" é configurada na base de dados
    When eu enviar uma requisição `PUT` para "/api/cities/BD" com o seguinte corpo:
    Then o código de status da resposta deve ser 201
    And a resposta deve ser um objeto `JSON`
    And o objeto deve ser igual ao seguinte:
      | campo | valor |
      | id    | "cities/BD" | 

  Scenario: 5. Atualizar parcialmente uma cidade
    Given que a url base da API é "https://fooapi.com"
    And que o endpoint para cidades é "/api/cities"
    And que a cidade "BD" é configurada na base de dados
    When eu enviar uma requisição `PATCH` para "/api/cities/BD" com o seguinte corpo:
    Then o código de status da resposta deve ser 201
    And a resposta deve ser um objeto `JSON`
    And o objeto deve ser igual ao seguinte:
      | campo | valor |
      | id    | "BD" |

  Scenario: 6. Deletar uma cidade
    Given que a url base da API é "https://fooapi.com"
    And que o endpoint para cidades é "/api/cities"
    And que a cidade "BD" é configurada na base de dados
    When eu enviar uma requisição `DELETE` para "/api/cities/BD"
    Then o código de status da resposta deve ser 200
    And a resposta deve ser um objeto `JSON`
    And o objeto deve ser igual ao seguinte:
      | campo | valor |
      | id    | "None" | 