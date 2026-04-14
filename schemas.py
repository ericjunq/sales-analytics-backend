from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from security.validations import CNPJ, Telefone
from datetime import datetime

# Empresa
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
    updated_at: Optional[datetime] = None

# Requisições de dados

class DefinicaoColunas(BaseModel):
    name: str 
    type: Literal['numeric', 'object', 'bool']

class AnaliseRequest(BaseModel):
    coluna_ativo: str  # nome da coluna
    valor_ativo: str # exemplo 1 ou True representam ativo
    colunas: list[DefinicaoColunas]

