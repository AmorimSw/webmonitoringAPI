import requests
from .utils.dataTreatment import personDataTreatment, companyDataTreatment

def _generate_token():

    url = "https://api.assertivasolucoes.com.br/oauth2/v3/token/"

    payload = 'grant_type=client_credentials'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic WmpZeFlqSmhNbU5oWVdRMk56TTNORE13T1RJMU5qUXpOekl5TUdOa09ETWdJQzBLOllXTTVORE14WkdGaVlUbGxNVEF4WWpkbVpXVm1ZakF3TXpZNU5XRmhORFVnSUMwSw=='
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    barear_token = response.json()
    return barear_token['access_token']

# =======================
# Consultas Pessoa Física
# =======================

def cpf_request(cpf:str):
    barear_token = _generate_token()

    url = f"https://api.assertivasolucoes.com.br/localize/v3/cpf/?cpf={cpf}&idFinalidade=1"

    payload = {}
    headers = {
    'authorization': barear_token,
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response.raise_for_status()

    personData = personDataTreatment(response.json())

    return personData

# =========================
# Consultas Pessoa Jurídica
# =========================

def cnpj_request(cnpj:str) -> dict:
    barear_token = _generate_token()
    url = f"https://api.assertivasolucoes.com.br/localize/v3/cnpj/?cnpj={cnpj}&idFinalidade=1"

    payload = {}
    headers = { 'Authorization': barear_token }

    response = requests.request("GET", url, headers=headers, data=payload)
    response.raise_for_status()

    companyData = companyDataTreatment(response.json())
    return companyData

# =============================
# Consulta Pessoas Relacionadas
# =============================

def related_people_request(documento:str=None):
    if not documento:
        return

    request_type = 'CPF' if len(documento) == 11 else "CNPJ"

    barear_token = _generate_token()
    url = 'https://api.assertivasolucoes.com.br/localize-api/v1/base-cadastral/conexoes'

    headers = {
        'Authorization' : barear_token,
    }

    params = {
        'documento' : documento,
        'tipo' : request_type,
        'idFinalidade' : 1,
        'conjugue' : True
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    return response.json()

    