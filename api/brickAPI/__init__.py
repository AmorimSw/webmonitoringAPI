import json
import os
import requests

from time import sleep

def __create_token() -> dict:
    url = "https://api.brickseguros.com.br/auth"

    headers = {
        'Authorization': os.environ.get('BRICK_API_KEY'),
        'accept': 'application/json',
    }

    response = requests.post(
        url,
        headers=headers
    )

    data = response.json()
    return data['token']

def _get_pf_research_protocol(cpf:str) -> str:
    bearer_token = __create_token()

    cpf = ''.join([c for c in cpf if c.isnumeric()])

    headers = {
    'Authorization' : 'Bearer ' + bearer_token       
    }
    body = {
        'document' : cpf,
        'entity_type' : 'PF',
        'bundles' : ['ESSENTIAL']
    }

    response = requests.post(
        'https://api.brickseguros.com.br/v1/record',
        headers=headers,
        json=body
    )
    if response.status_code == 201 or response.status_code == 200:
        return response.json()['data']['id']

    response.raise_for_status()

def get_pf_research_results(cpf:str) -> dict:
    research_id = _get_pf_research_protocol(cpf)

    sleep(10)

    bearer_token = __create_token()
    headers = {
        'Authorization' : 'Bearer ' + bearer_token
    }
    
    response = requests.get(
        f'https://api.brickseguros.com.br/v1/record/{research_id}',
        headers=headers
    )
    if response.status_code == 201 or response.status_code == 200:
        return response.json()

    response.raise_for_status()