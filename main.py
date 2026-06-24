from fastapi import FastAPI, HTTPException
from firebase_admin import credentials, initialize_app, firestore
from datetime import datetime
import dotenv, os

dotenv.load_dotenv()
app = FastAPI(debug=True)

@app.get('/')
def root():
    return {200 : 'Sucesso'}

@app.get('/api/teste')
def searchOpenSanctiopns():
    return {}