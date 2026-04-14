from pydantic import BaseModel, EmailStr
from typing import Optional
from security.validations import CNPJ, Telefone
from datetime import datetime

class EmpresaSchema(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    cnpj: CNPJ
    telefone: Telefone

class EmpresaResponse(BaseModel):
    id: int 
    nome: str
    cnpj: CNPJ
    created_at: datetime
    updated_at: datetime