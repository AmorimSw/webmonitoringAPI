import requests
import os

def requestInquiriesInfos(startDate:str, endDate:str):
    '''Conexão direta com o SCi2 para fazer a requisição de informações sobre os pedidos de sindicâncias'''

    BASE_URL = "https://api-sci2.swint.com.br/auth/inquiry/list/json"
    API_KEY = os.getenv('SCI2_API_KEY')

    headers = {
        'x-api-key' : API_KEY
    }

    params = {
        'startDate' : startDate,
        'endDate' : endDate
    }

    response = requests.get(BASE_URL, headers=headers, params=params)

    return response.json()

