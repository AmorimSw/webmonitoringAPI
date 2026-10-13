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




# Filtro para visualizar apenas processos
# def get_only_law_suits(research_result):
#     analyses = research_result['data']['analyses']

#     law_suits = []
#     for i, analysis in enumerate(analyses):
#         if analysis['type'] == 'PF_LAW_SUITS' or analysis['type'] == 'PJ_LAW_SUITS':
#             law_suit = dict()
#             infos:dict = json.loads(analysis.get('content', {}))

#             if not infos:
#                 continue

#             for k in infos.keys():
#                 try:
#                     law_suit[k] = []

#                     for proc_infos in infos[k]:
#                         proccess = dict()
#                         proccess['numero_processo'] = proc_infos['lawsuit_nr']
#                         proccess['tribunal'] = proc_infos['court']
#                         proccess['tipo'] = proc_infos['branch']
#                         proccess['segredo_justica'] = proc_infos['justice_secret']
#                         proccess['criminal'] = proc_infos['is_criminal']
#                         proccess['tipo_criminal'] = proc_infos['crime_type']
#                         proccess['status'] = proc_infos['status']
#                         proccess['valor'] = proc_infos['value']
#                         proccess['reclamante'] = proc_infos['authors']
#                         proccess['advogados'] = proc_infos['neutral']
#                         proccess['reclamado'] = proc_infos['defendands']

#                         law_suit[k].append(proccess)

#                 except Exception:
#                     continue

#             law_suits.append(law_suit)
#     return law_suits