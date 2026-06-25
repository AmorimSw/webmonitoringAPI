from typing import List
import re

def _checkSanction(datasets:list) -> bool:
    for data in datasets:
        if re.search('sanctions', data):
            return True
    return False
    
def visualizeMatchInfo(responseJson:dict) -> List[dict]:
    response = responseJson['responses']['query']['results']

    lista_respostas = []
    for result in response:
        resposta = dict()

        result_caption = result.get('caption', {})
        result_schema = result.get('schema', {})
        result_properties = result.get('properties', {})

        result_taxNumber = []
        result_topics = []
        result_citizenship = []
        if result_properties:
            result_taxNumber = result_properties.get('taxNumber', {})
            result_topics = result_properties.get('topics', {})
            result_citizenship = result_properties.get('citizenship', {})

        result_datasets = result.get('datasets', {})
        result_referents = result.get('referents', {})

        resposta['caption'] = result_caption
        resposta['schema'] = result_schema
        # resposta['properties'] = result_properties
        resposta['taxNumber'] = result_taxNumber
        resposta['topics'] = result_topics
        resposta['citizenship'] = result_citizenship
        resposta['datasets'] = result_datasets
        resposta['checkSanction'] = _checkSanction(result_datasets)
        resposta['referents'] = result_referents

        lista_respostas.append(resposta)

    return lista_respostas