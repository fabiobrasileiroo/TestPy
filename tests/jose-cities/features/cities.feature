Feature: Cities API - José

  Scenario: Listar todas as cidades
    Given que a url base da API é "https://fooapi.com"
    When eu fizer uma requisição GET para "/api/cities"
    Then o código de status da resposta deve ser 200
    And o JSON deve conter "features"
    And cada feature deve ter os campos "id,properties,geometry"

  Scenario: Buscar cidade por ID
    Given que a url base da API é "https://fooapi.com"
    And existe um id de cidade "BR"
    When eu fizer uma requisição GET para "/api/cities/BR"
    Then o código de status da resposta deve ser 200
    And o JSON deve conter "data"
    And dentro de data as propriedades devem ter "city,country,iso2,iso3"
