import requests

class BacenSanctionsAPI:

    def __init__(self):
        pass

    def _requestData(self) -> dict:
        response = requests.get(
            'https://www.bcb.gov.br/api/servico/sitebcb/Regesp_Internet?filtro=((Cnpj%20ne%20null))',
        )
        response.raise_for_status()

        return response.json()['conteudo']
    
    def requestBacenSanction(self, cnpj):
        sanctions_data = self._requestData()

        for sanction in sanctions_data:
            if sanction['Cnpj'] == cnpj:
                result = dict()
                result['razaoSocial'] = sanction['NomeIf']
                result['cnpj'] = cnpj
                result['segmento'] = sanction['Segmento']
                result['tipoRegime'] = sanction['Segmento']
                result['dataInicio'] = sanction['DataInicioRegime']
                result['dataFinal'] = sanction['DataFimRegime']

                return result