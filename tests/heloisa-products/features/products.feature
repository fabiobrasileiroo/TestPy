# language: pt
Funcionalidade: Products API - Heloisa

  Contexto:
    Dado que a url base da API é "https://fooapi.com"
    E que o endpoint para listar produtos é "/api/products"

# 1. Listar músicas – GET /api/products
  Cenário: Listar todas os produtos
    Quando eu enviar uma requisição `GET` para "/api/products"
    Então o código de status da resposta deve ser 200
    E a resposta deve ser um array de `JSON`
    E o array deve conter pelo menos 1 produto
    E cada produto deve ter os campos "id", "title", "description", "brand", "category", "price", "rating" e "stock"
    E a resposta deve conter o seguinte produto com um array de objetos com os seguintes valores:
      | campo       | valor                                                                                                                                           |
      | id          | 1                                                                                                         |
      | title       | Vertical Herb Garden Kit with LED Grow Lights                                                             |
      | description | Grow fresh herbs year-round, even in limited space! This vertical herb garden kit utilizes a compact design with tiered planters. Integrated LED grow lights provide optimal light conditions for your herbs, ensuring healthy growth regardless of natural light availability. |
      | brand       | UrbanSprout                                                                                               |
      | category    | Gardening                                                                                                |
      | price       | 19.2                                                                                                     |
      | rating      | 2.5                                                                                                      |
      | stock       | 13                                                                                                       |

# 2. Listar produto por ID - GET /api/products/{id}
  Cenário: Listar um produto pelo seu ID
    Dado que existe um produto com id "1"
    Quando eu enviar uma requisição `GET` para "/api/products/1"
    Então o código de status da resposta deve ser 200
    E a resposta dessa requisição deve ser um objeto `JSON`
    E o objeto deve ter os campos "id", "title", "description", "brand", "category", "price", "rating" e "stock"
    E o objeto deve ser igual ao seguinte:
      | campo       | valor                                                                                                                                           |
      | id          | 1                                                                                                         |
      | title       | Vertical Herb Garden Kit with LED Grow Lights                                                             |
      | description | Grow fresh herbs year-round, even in limited space! This vertical herb garden kit utilizes a compact design with tiered planters. Integrated LED grow lights provide optimal light conditions for your herbs, ensuring healthy growth regardless of natural light availability. |
      | brand       | UrbanSprout                                                                                               |
      | category    | Gardening                                                                                                |
      | price       | 19.2                                                                                                     |
      | rating      | 2.5                                                                                                      |
      | stock       | 13                                                                                                       |

# 3. Criar produto - POST /api/products
  Cenário: Criar um produto
    Quando eu enviar uma requisição `POST` para "/api/products" com o seguinte corpo:
      """json
      {
          "title": "Foo title",
          "description": "Foo desc",
          "brand": "Foo Brand",
          "category": "Fooooooo",
          "price": 19.2,
          "rating": 2.5,
          "stock": 13
      }
      """
    Então o código de status da resposta deve ser 201
    E a resposta deve ser um objeto `JSON`
    E o objeto deve ter os campos "id", "title", "description", "brand", "category", "price", "rating" e "stock"
    E a resposta deve ser um objeto com os seguintes valores:
      | campo       | valor     |
      | id          | "31"      |
      | title       | Foo title |
      | description | Foo desc  |
      | brand       | Foo Brand |
      | category    | Fooooooo  |
      | price       | 19.2      |
      | rating      | 2.5       |
      | stock       | 13        |

# 4. Atualizar produto - PUT /api/products/{id}
  Cenário: Atualizar produto com um id existente
    Dado que existe um produto com id "1"
    Quando eu enviar uma requisição `PUT` para "/api/products/1" com o seguinte corpo:
      """json
      {
          "title": "Footitle",
          "description": "Foodesc",
          "brand": "FooBrand",
          "category": "Fooooooo",
          "price": 19.2,
          "rating": 2.5,
          "stock": 13
      }
      """
    Então o código de status deve ser 201
    E a resposta deve ser um objeto `JSON`
    E o objeto deve ter os campos "id", "title", "description", "brand", "category", "price", "rating" e "stock"
    E o objeto deve ser igual ao seguinte:
      | campo       | valor     |
      | id          | 1         |
      | title       | Footitle  |
      | description | Foodesc   |
      | brand       | FooBrand  |
      | category    | Fooooooo  |
      | price       | 19.2      |
      | rating      | 2.5       |
      | stock       | 13        |

# 5. Atualizar parcialmente produto - PATCH /api/products/{id}
  Cenário: Atualizar parcialmente um produto existente
    Dado que existe um produto com id "1"
    Quando eu enviar uma requisição `PATCH` para "/api/products/1" com o seguinte corpo:
      """json
      {
          "price": 25.5,
          "stock": 20
      }
      """
    Então o código de status da resposta deve ser 201
    E a resposta deve ser um objeto `JSON`
    E o objeto deve ter os campos "id", "price" e "stock"
    E o objeto deve ser igual ao seguinte:
      | campo | valor |
      | id    | 1     |
      | price | 25.5  |
      | stock | 20    |

# 6. Deletar produto - DELETE /api/products/{id}
  Cenário: Deletar produto com um id existente
    Dado que existe um produto com id "1"
    Quando eu enviar uma requisição `DELETE` para "/api/products/1"
    Então o código de status da resposta deve ser 200
    E a resposta deve ser um objeto com os seguinte valores:
      | campo | valor |
      | id    | "1"   |