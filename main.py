from fastapi import FastAPI, HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from api import OpenSanctionsAPI, BacenSanctionsAPI, cpf_request, cnpj_request, vehicleDataRequest, email_request, phone_request, name_address_request, vehicle_history_request, extra_data_request, score_request
from api.sci2Api import requestInquiriesInfos
from typing import Literal
from datetime import datetime, date
import dotenv, os

dotenv.load_dotenv()
OsAPI = OpenSanctionsAPI()
BacenAPI = BacenSanctionsAPI()

app = FastAPI(
    debug=True
    )

API_KEY_NAME = 'x-api-key'
api_key_header = APIKeyHeader(name=API_KEY_NAME)

async def checkApiKey(apiKey: str = Security(api_key_header)):
    correctApiKey = os.environ['INTERNAL_API_KEY']
    if apiKey == correctApiKey:
        return apiKey
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Acesso negado: Api key inválida ou ausente."
    )

@app.get('/api/consultaSancoes/v1')
def searchSanctions(query:str, schema:Literal['Thing', 'Person', 'Company'], apikey:str=Security(checkApiKey)):
    """Parameters:
    * Schema: *Thing*, *Person*, *Company*
    O schema definirá será a pesquisa será sobre pessoas ou empresas. Mantendo como *Thing*,
    efetuará a pesquisa tanto de pessoas, quanto empresas."""
    assert schema in ['Thing', 'Person', 'Company']
    assert query is not None

    response = OsAPI.requestMatchInfo(schema=schema, query=query)

    return response

@app.get('/api/consultaSancoes/v2')
def searchSanctionsV2(query:str, schema:Literal['Thing', 'Person', 'Company'], apikey:str=Security(checkApiKey)):
    """Parameters:
    * Schema: *Thing*, *Person*, *Company*
    O schema definirá será a pesquisa será sobre pessoas ou empresas. Mantendo como *Thing*,
    efetuará a pesquisa tanto de pessoas, quanto empresas.
    """
    assert schema in ['Thing', 'Person', 'Company']
    assert query is not None

    response = OsAPI.requestMatchInfoV2(schema=schema, query=query)

    return response

@app.get('/api/consultaSancoesBacen')
def searchBacenSanctions(cnpj, apikey:str=Security(checkApiKey)):
    """
    """

    response = BacenAPI.requestBacenSanction(cnpj)

    return response

@app.get('/api/consultaPessoaAssertiva')
def searchPersonInfosAssertiva(document, apikey:str=Security(checkApiKey)):
    """Realiza a consulta de uma pessoa física na base de dados do Assertiva."""
    response = cpf_request(document)
    return response

@app.get('/api/consultaEmpresaAssertiva')
def searchCompanyInfosAssertiva(document, apikey:str=Security(checkApiKey)):
    """Realiza a consulta de uma jurídica na base de dados do Assertiva."""
    response = cnpj_request(document)
    return response

@app.get('/api/consultaEmailAssertiva')
def searchEmailInfosAssertiva(email, apikey:str=Security(checkApiKey)):
    """Realiza a consulta de e-mail na base de dados do Assertiva."""
    response = email_request(email)
    return response

@app.get('/api/consultaTelefoneAssertiva')
def searchPhoneInfosAssertiva(telefone, apikey:str=Security(checkApiKey)):
    """Realiza a consulta de telefone na base de dados do Assertiva."""
    response = phone_request(telefone)
    return response

@app.get('/api/consultaEnderecoNome')
def searchNameAddressInfosAssertiva(nomeOuRazaoSocial: str, buscarPor, cepOuNomeRua, bairro, cidade, uf, nomeOuRazaoSocialExata=False, apikey:str=Security(checkApiKey)):
    """Realiza a consulta de nome e endereço na base de dados do Assertiva."""
    response = name_address_request(nomeOuRazaoSocial, buscarPor, cepOuNomeRua, bairro, cidade, uf, nomeOuRazaoSocialExata)
    return response

@app.get('/api/consultaVeiculoAssertiva')
def searchVehicleInfosAssertiva(vehiclePlate, apikey:str=Security(checkApiKey)):
    """Realiza a consulta de veículos e proprietário com base no emplacamento."""
    response = vehicleDataRequest(vehiclePlate)
    return response

@app.get('/api/propietarioVeiculo')
def searchVehicleHistoryInfosAssertiva(document: str, apikey:str=Security(checkApiKey)):
    """Realiza a consulta do histórico de veículos na base de dados do Assertiva."""
    response = vehicle_history_request(document)
    return response


@app.get('/api/sci2/reqSindicancia')
def requestInquiries(startDate:date, endDate:date, apikey:str=Security(checkApiKey)):
    """Consulta base de sindicâncias com base em um período de datas.
    As datas devem ser enviadas em formato de yyyy-mm-dd."""

    response = requestInquiriesInfos(startDate, endDate)
    return response

@app.get('/api/dadosExtras/pessoas')
def searchExtraDataAssertiva(cpf: str, retornarMae: bool = True, apikey:str=Security(checkApiKey)):
    """Realiza a consulta de conexões na base de dados do Assertiva."""
    response = extra_data_request(cpf, retornarMae)
    return response

@app.get('/api/score')
def searchScoreAssertiva(cpf: str, apikey:str=Security(checkApiKey)):
    """Realiza a consulta de Score (Mix-V3 PF) na base de dados do Assertiva."""
    response = score_request(cpf)
    return response