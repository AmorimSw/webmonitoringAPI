import dotenv
import json
import os
import requests

from time import sleep
from typing import Literal

dotenv.load_dotenv()

'''
As consultas da Brick são realizadas em dois tempos: o primeiro você solicita o protocolo
(requisição _post_), momento em que as consultas são iniciadas por eles. Aproximadamente 10s
depois, as consultas são finalizadas, momento em que é realizada a coleta dos dados (requisição GET)
'''

def _create_token() -> dict:
    'Cria o token para a realização da consulta.'

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

def _get_pf_research_protocol(document, entity_type, bundles) -> str:
    bearer_token = _create_token()

    document = ''.join([c for c in document if c.isnumeric()])

    headers = {
    'Authorization' : 'Bearer ' + bearer_token       
    }
    body = {
        'document' : document,
        'entity_type' : entity_type,
        'bundles' : bundles
    }

    response = requests.post(
        'https://api.brickseguros.com.br/v1/record',
        headers=headers,
        json=body
    )
    if response.status_code == 201 or response.status_code == 200:
        return response.json()['data']['id']

    response.raise_for_status()

def get_pf_research_results(
        document:str,
        entity_type:Literal['PF', 'PJ'],
        bundles:Literal[
                'ESSENTIAL', 'BOA_VISTA', 'SERASA', 'SPC', 'LIVENESS',
                'PUBLIC_JOBS', 'SOCIAL_ASSISTANCE', 'CLASS_ENTITIES', 'KYC',
            ]=['ESSENTIAL']
) -> dict:
    '''
    Criação do protocolo de pesquisas do Brick.
    - document - String - Documento CPF ou CNPJ;
    - entity_type - String - _PF_ ou _PJ_, define se os levantamentos serão realizados sobre PF ou PJ;
    - bundles - List[String] - Define quais serão os levantamentos realizados pela Brick. Por padrão, será feito apenas o _ESSENTIAL_.
    Maiores detalhes sobre os _bundles_: https://docs.brickseguros.com.br/reference/record-1
    '''
    
    research_id = _get_pf_research_protocol(document, entity_type, bundles)

    sleep(10)

    bearer_token = _create_token()
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