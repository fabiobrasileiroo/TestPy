import requests

def test_insert_employee():
    headers = {
        'Accept': '*/*',
        'User-Agent': 'request'
    }

    url = 'http://dummy.restapiexample.com/api/v1/create'

    new_employee = {'name':'Testerson','salary':'5000','age':'32'}

    resposta = requests.post(url, headers=headers, data=new_employee)
    resposta_dict = resposta.json()

    if resposta.status_code == 200:
        status = resposta_dict['status']
        employee_response = resposta_dict['data']

        assert status == 'success' and employee_response['id'] is not None
    else:
        assert False