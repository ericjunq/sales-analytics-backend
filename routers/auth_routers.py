from fastapi import APIRouter, HTTPException, Depends
from dependencies import get_db
from security.security import criptografar_senha, verificar_senha, criar_access_token, criar_refresh_token, get_current_empresa
from schemas import EmpresaResponse, EmpresaSchema
from sqlalchemy.orm import Session
from models import Empresa
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix='/empresa', tags=['empresa'])

@auth_router.post('/cadastro', response_model=EmpresaResponse)
async def cadastrar_empresa(
    empresaschema: EmpresaSchema,
    db: Session = Depends(get_db)
):
    email_existente = db.query(Empresa).filter(Empresa.email == empresaschema.email).first()
    if email_existente:
        raise HTTPException(status_code=404, detail='Email já cadastrado')
    
    cnpj_existente = db.query(Empresa).filter(Empresa.cnpj == empresaschema.cnpj).first()
    if cnpj_existente:
        raise HTTPException(status_code=404, detail='CNPJ já cadastrado')
    
    telefone_existente = db.query(Empresa).filter(Empresa.telefone == empresaschema.telefone).first()
    if telefone_existente:
        raise HTTPException(status_code=404, detail='Telefone já cadastrado')
    
    senha_criptografada = criptografar_senha(empresaschema.senha)

    empresa = Empresa(
        nome = empresaschema.nome, 
        email = empresaschema.email,
        senha_hash = senha_criptografada, 
        cnpj = empresaschema.cnpj,
        telefone = empresaschema.telefone
    )

    db.add(empresa)
    db.commit()
    db.refresh(empresa)

    return empresa

@auth_router.post('/login')
async def login(
    dados: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    empresa = db.query(Empresa).filter(
        Empresa.email == dados.username
    ).first()
    if empresa is None:
        raise HTTPException(status_code=404, detail='Email não encontrado')
    
    if not verificar_senha(dados.password, empresa.senha_hash):
        raise HTTPException(status_code=401, detail='Senha incorreta')
    
    access_token = criar_access_token(
        data = {'sub': dados.username, 'type': 'access'}
    )

    refresh_token = criar_refresh_token(
        data = {'sub': dados.username, 'type': 'refresh'}
    )

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer'
    }