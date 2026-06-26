from fastapi import FastAPI, HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from api import OpenSanctionsAPI
from datetime import datetime
import dotenv, os

dotenv.load_dotenv()
OsAPI = OpenSanctionsAPI()

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
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Acesso negado: Api key inválida ou ausente."
    )


@app.get('/')
def root():
    return {200 : 'Sucesso'}

@app.get('/api/consultaSancoes/v1')
def searchSanctions(schema:str, query:str, apikey:str=Security(checkApiKey)):
    """Parameters:
    * Schema: *Thing*, *Person*, *Company*
    O schema definirá será a pesquisa será sobre pessoas ou empresas. Mantendo como *Thing*,
    efetuará a pesquisa tanto de pessoas, quanto empresas."""
    assert schema in ['Thing', 'Person', 'Company']
    assert query is not None

    response = OsAPI.requestMatchInfo(schema=schema, query=query)

    return response

@app.get('/api/consultaSancoes/v2')
def searchSanctionsV2(schema:str, query:str, apikey:str=Security(checkApiKey)):
    """Parameters:
    * Schema: *Thing*, *Person*, *Company*
    O schema definirá será a pesquisa será sobre pessoas ou empresas. Mantendo como *Thing*,
    efetuará a pesquisa tanto de pessoas, quanto empresas.
    """
    assert schema in ['Thing', 'Person', 'Company']
    assert query is not None

    response = OsAPI.requestMatchInfoV2(schema=schema, query=query)

    return response
