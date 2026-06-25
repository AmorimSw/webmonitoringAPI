import requests, os
from typing import Literal

class OpenSanctionsAPI:

    def __init__(self):
        self.BASE_URL = "https://api.opensanctions.org"
        self.API_KEY = os.environ.get('OPEN_SANCTIONS_KEY')

        self.session = requests.Session()
        self.session.headers['Authorization'] = f'ApiKey {self.API_KEY}'

    def request_match_info(self, query:str, schema:Literal['Person', 'Company', 'Thing']='Thing'):

        query_schema = {
            'queries' : {
                'query' : {
                    'schema' : schema,
                    'properties' : {
                       'name' : [query]
                    }
                }
            }
        }

        response = self.session.post(f'{self.BASE_URL}/match/default', json=query_schema)
        response.raise_for_status()

        return response.json()