from fastapi import FastAPI, HTTPException
from firebase_admin import credentials, initialize_app, firestore

app = FastAPI()
cred = credentials.Certificate('testeenviodados-firebase-adminsdk-fbsvc-62891af769.json')
initialize_app(cred)

@app.post('/api/customers/new', status_code=201)
def insert_newCustomer(customerName:str, customerSegment:str):
    """Registra um novo cliente no firestore."""
    
    try:
        customerInfos = {
            'customerName' : customerName,
            'customerSegment' : customerSegment
        }
        db = firestore.client()
        db.collection('customers').add(customerInfos)
        return 'Cliente inserido com sucesso!'
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)
    
@app.get('/api/customers/getAll', status_code=200)
def get_customersList() -> list:
    """Recebe uma lista contendo informações de clientes inseridos no banco de dados.\n
    Incluindo:
    * Nome do cliente
    * Semgmento de atuação"""

    db = firestore.client()
    customers_ref = db.collection('customers')
    customers = [customer.to_dict() for customer in customers_ref.stream()]

    return customers

@app.post('/api/crawler/keywordSearch/new', status_code=201)
def insert_newKeywordSearch(customerName:str, keywordSearch:str, classification:str):
    """Insere uma nova palavra-chave para ser pesquisada."""

    try:
        newKeyword = {
            'customerName' : customerName,
            'search' : keywordSearch,
            'classification' : classification
        }

        db = firestore.client()
        db.collection('crawlerKeywords').add(newKeyword)
        return 'Palavra-chave inserida com sucesso.'
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)

@app.get('/api/crawler/keywordSearch/get')
def get_keywordsSearchList() -> list:
    """Recebe uma lista contendo todas as palavras-chave para busca.
    
    Incluindo:
    * Nome do cliente
    * Palavra-chave de busca
    * Classificação da palavra-chave
    """

    db = firestore.client()
    keywords_ref = db.collection('crawlerKeywords')
    keywords = [keyword.to_dict() for keyword in keywords_ref.stream()]

    return keywords

@app.post('/api/crawler/insertNewInfo', status_code=201)
def crawler_insertInfo(crawlerInfo:dict):
    """Insere informações encontradas por Crawlers no banco de dadoss"""

    try:
        db = firestore.client()
        db.collection('crawlerInfoReports').add(crawlerInfo)    
        return 'Informação inserida com sucesso.'

    except Exception as e:
        raise HTTPException(status_code=400, detail=e)