import requests
from typing import Literal
from .utils.dataTreatment import personDataTreatment, companyDataTreatment, emailDataTreatment, phoneDataTreatment, nameAddressDataTreatment, vehicleHistoryDataTreatment, extraDataTreatment, scoreDataTreatment

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

# =========================
# Consultas E-mail
# =========================

def email_request(email:str):
    import urllib.parse
    barear_token = _generate_token()
    
    email_encoded = urllib.parse.quote(email)

    url = f"https://api.assertivasolucoes.com.br/localize/v3/email/?email={email_encoded}&idFinalidade=1"

    payload = {}
    headers = {
    'authorization': barear_token,
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response.raise_for_status()

    emailData = emailDataTreatment(response.json())

    return emailData

# =========================
# Consultas Telefone
# =========================

def phone_request(telefone:str):
    import urllib.parse
    barear_token = _generate_token()
    
    telefone_encoded = urllib.parse.quote(telefone)

    url = f"https://api.assertivasolucoes.com.br/localize/v3/telefone/?telefone={telefone_encoded}&idFinalidade=1"

    payload = {}
    headers = {
    'authorization': barear_token,
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response.raise_for_status()

    phoneData = phoneDataTreatment(response.json())

    return phoneData

# =========================
# Consultas Nome ou Endereço
# =========================

def name_address_request(nomeOuRazaoSocial:str, buscarPor:Literal['ambas', 'pessoas', 'empresas']='ambas', cepOuNomeRua:str=None, bairro:str=None, cidade:str=None, uf:str=None, nomeOuRazaoSocialExata:bool=False):
    import urllib.parse
    barear_token = _generate_token()
    
    nome_encoded = urllib.parse.quote(nomeOuRazaoSocial)

    url = f"https://api.assertivasolucoes.com.br/localize/v3/nome-endereco/"

    payload = {}
    headers = {
    'authorization': barear_token,
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    params = {
        'buscarPor' : buscarPor,
        'nomeOuRazaoSocial' : nomeOuRazaoSocial.upper(),
        'idFinalidade' : 1,
    }

    if nomeOuRazaoSocialExata:
        params['nomeOuRazaoSocialExata'] = nomeOuRazaoSocialExata

    if cepOuNomeRua:
        params['cepOuNomeRua'] = cepOuNomeRua

    if bairro:
        params['bairro'] = bairro.upper()

    if cidade:
        params['cidade'] = cidade.upper()
    
    if uf:
        params['uf'] = uf.upper()


    response = requests.request("GET", url, headers=headers, data=payload, params=params)
    

    nameAddressData = nameAddressDataTreatment(response.json())

    return nameAddressData

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

# =================================
# Consulta Veículos e Proprietários
# =================================

def _vehicleProtocolRequest(placa) -> str:
    barear_token = _generate_token()

    url = 'https://api.assertivasolucoes.com.br/veiculos/v3/consulta-base'

    headers = {
        'Authorization' : barear_token
    }

    params = {
        'idFinalidade' : 2,
        'documento' : placa,
        'tipo' : 'placa'
    }

    response = requests.get(url, headers=headers, params=params)
    resp_json = response.json()

    protocolo = resp_json.get('cabecalho', {}).get('protocolo', '')
    return protocolo

def vehicleDataRequest(placa) -> dict:
    barear_token = _generate_token()

    protocolo = _vehicleProtocolRequest(placa)

    url = 'https://api.assertivasolucoes.com.br/veiculos/v3/demais-consultas'

    headers = {
        'Authorization' : barear_token
    }

    params = {
        'idFinalidade' : 2,
        'consulta' : 'binestadual',
        'documento' : placa,
        'tipo' : 'placa',
        'protocolo' : protocolo
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json()

# =================================
# Histórico de Veículos
# =================================

def vehicle_history_request(document:str):
    barear_token = _generate_token()

    url = f"https://api.assertivasolucoes.com.br/veiculos/v3/historico-veiculos"

    payload = {}
    headers = {
        'authorization': barear_token,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    params = {
        'documento' : document,
        'idFinalidade' : 2,
    }

    response = requests.request("GET", url, headers=headers, data=payload, params=params)
    

    vehicleHistoryData = vehicleHistoryDataTreatment(response.json())

    return vehicleHistoryData

# =================================
# Consulta Dados Extras (Conexões)
# =================================

def extra_data_request(cpf:str, retornarMae:bool=True):
    barear_token = _generate_token()

    url = "https://api.assertivasolucoes.com.br/localize/v3/pessoas-de-referencia"

    payload = {}
    headers = {
        'authorization': barear_token,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    params = {
        'cpf': cpf,
        'retornarMae': str(retornarMae).lower(),
        'idFinalidade': 1,
    }

    response = requests.request("GET", url, headers=headers, data=payload, params=params)
   

    extraData = extraDataTreatment(response.json())

    return extraData

# =================================
# Consulta Mix (Score)
# =================================

def score_request(cpf:str):
    barear_token = _generate_token()

    url = f"https://api.assertivasolucoes.com.br/mix-v3/pf/{cpf}"

    payload = {}
    headers = {
        'authorization': barear_token,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    params = {
        'idFinalidade': 2,
    }

    response = requests.request("GET", url, headers=headers, data=payload, params=params)    

    scoreData = scoreDataTreatment(response.json())

    return scoreData
