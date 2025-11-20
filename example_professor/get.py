import requests  # Importa a biblioteca para fazer requisições HTTP

# Define cabeçalhos da requisição
headers = {
    'Accept': '*/*',  # Aceita qualquer tipo de resposta
    'User-Agent': 'request',  # Identifica o cliente que faz a requisição
}

# URL da API de exemplo
url = "http://dummy.restapiexample.com/api/v1/employees"

# Envia a requisição GET para a API
resposta = requests.get(url, headers=headers)

# Exibe o conteúdo da resposta (normalmente em formato JSON)
print(resposta.text)


