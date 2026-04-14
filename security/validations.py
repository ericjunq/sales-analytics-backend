import re
from pydantic import AfterValidator
from typing import Annotated

def validar_telefone(telefone: str) -> bool:
    padrao = r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$'
    if re.match(padrao, telefone):
        return True
    return False

def validar_cnpj(cnpj: str) -> bool:
    cnpj = cnpj.replace(".", "").replace("/", "").replace("-", "")
    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False
    pesos = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    total = sum(int(cnpj[i]) * pesos[i] for i in range(12))
    remainder = total % 11
    primeiro = 0 if remainder < 2 else 11 - remainder
    if primeiro != int(cnpj[12]):
        return False
    pesos = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    total = sum(int(cnpj[i]) * pesos[i] for i in range(13))
    remainder = total % 11
    segundo = 0 if remainder < 2 else 11 - remainder
    if segundo != int(cnpj[13]):
        return False
    return True

# --- Checadores (levantam erro se inválido) ---

def checar_cnpj(v: str) -> str:
    if not validar_cnpj(v):
        raise ValueError('CNPJ inválido')
    return v

def checar_telefone(v: str) -> str:
    if not validar_telefone(v):
        raise ValueError('Telefone inválido')
    return v

# --- Tipos reutilizáveis ---
CNPJ = Annotated[str, AfterValidator(checar_cnpj)]
Telefone = Annotated[str, AfterValidator(checar_telefone)]