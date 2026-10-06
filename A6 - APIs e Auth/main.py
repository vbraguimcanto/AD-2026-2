from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import os
import requests
import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, auth


load_dotenv()
app = FastAPI()
API_KEY = os.getenv("FIREBASE_API_KEY")
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)
security = HTTPBearer()


class Usuario(BaseModel):
    email: str
    senha: str


@app.post("/usuarios")
def criar_usuario(usuario: Usuario):
    try:
        novo_usuario = auth.create_user(email=usuario.email, password=usuario.senha)
        return {
            "uid": novo_usuario.uid,
            "email": novo_usuario.email
        }

    except Exception:
        raise HTTPException(status_code=400, detail="Não foi possível criar o usuário")


@app.post("/login")
def login(usuario: Usuario):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    dados = {
        "email": usuario.email,
        "password": usuario.senha,
        "returnSecureToken": True
    }
    resposta = requests.post(url, json=dados)
    if resposta.status_code != 200:
        raise HTTPException(status_code=401, detail="Email ou senha inválidos")

    return {
        "token": resposta.json()["idToken"]
    }


def verificar_token(credenciais: HTTPAuthorizationCredentials = Depends(security)):
    token = credenciais.credentials
    try:
        usuario = auth.verify_id_token(token)
        return usuario
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")


@app.get("/perfil")
def perfil(usuario = Depends(verificar_token)):
    return {
        "uid": usuario["uid"],
        "email": usuario["email"]
    }