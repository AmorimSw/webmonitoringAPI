from fastapi import FastAPI, HTTPException
from api import OpenSanctionsAPI
from datetime import datetime
import dotenv, os

dotenv.load_dotenv()

app = FastAPI(
    debug=True
    )

OsAPI = OpenSanctionsAPI()

@app.get('/')
def root():
    return {200 : 'Sucesso'}

@app.get('/api/consultaSancoes')
def searchOpenSanctiopns(schema:str, query:str):
    assert schema in ['Thing', 'Person', 'Company']
    assert query is not None

    response = OsAPI.request_match_info(schema=schema, query=query)

    return response
