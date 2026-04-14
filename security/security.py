from pwdlib import PasswordHash
from jose import jwt, JWTError
from settings import settings
from datetime import datetime, timezone, timedelta
from fastapi.security import OAuth2PasswordBearer
from dependencies import get_db
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from models import Empresa

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/empresa/login')

password_hash = PasswordHash.recommended()

def criptografar_senha(senha: str)-> str:
    return password_hash.hash(senha)

def verificar_senha(senha: str, senha_hash: str)->bool: 
    return password_hash.verify(senha, senha_hash)

def criar_access_token(dados: dict):
    to_encode = dados.copy()
    expires = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expires_minutes)
    to_encode.update({'exp': expires})

    access_token = jwt.encode(
        to_encode,
        settings.secret_key,
        settings.algorithm
    )

    return access_token

def criar_refresh_token(dados:dict):
    to_encode = dados.copy()
    expires = datetime.now(timezone.now) + timedelta(days=settings.refresh_token_expires_days)
    to_encode.update({'exp': expires})

    refresh_token = jwt.encode(
        to_encode,
        settings.secret_key,
        settings.algorithm
    )

    return refresh_token

def get_current_empresa(
        token: str = Depends(oauth_scheme), 
        db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            [settings.algorithm]
        )
        email = payload.get('sub')
        if email is None:
            raise HTTPException(status_code=401, detail='Token inválido')
        
    except JWTError:
        raise HTTPException(status_code=401, detail='Token inválido')
    
    empresa = db.query(Empresa).filter(Empresa.email == email).first()
    if empresa is None:
        raise HTTPException(status_code=401, detail='Empresa não encontrada')
    
    return empresa