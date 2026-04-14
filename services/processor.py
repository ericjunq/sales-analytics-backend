import io
import pandas as pd
from schemas import DefinicaoColunas, AnaliseRequest


def ler_arquivo(
    file_bytes: bytes,
    filename: str
)-> pd.DataFrame:
    fim_arquivo = filename.split('.')[-1].casefold()
    if fim_arquivo == 'csv':
        df = pd.read_csv(io.BytesIO(file_bytes))
    elif fim_arquivo in ('xlsx', 'xls'):
        df = pd.read_excel(io.BytesIO(file_bytes))
    else:
        raise ValueError('Arquivo não suportado. Envie apenas Excel ou CSV')
    
    return df

def validar_colunas(
        df: pd.DataFrame, 
        colunas: list[DefinicaoColunas], 
        coluna_ativo: str
)-> pd.DataFrame:
    if colunas is None:
        raise ValueError('É necessário inserir pelo menos uma coluna')
    if coluna_ativo is None:
        raise ValueError('Coluna de Ativo/Status é obrigatória')
    
    nomes = [col.name for col in colunas] + [coluna_ativo]

    colunas_faltando = [col for col in colunas if not col in df.columns]
    if colunas_faltando:
        raise ValueError(f'Colunas {colunas_faltando} inexistentes ou não encontradas')

    df = df[nomes]

    return df

def filtro_analise_colunas(
        df: pd.DataFrame,
        request: AnaliseRequest
)-> dict:
    ativos = df[df[request.coluna_ativo]] == request.valor_ativo
    inativos = df[df[request.coluna.ativo]] != request.valor_ativo

    resultado = {}

    for coluna in request.colunas:
        if coluna.type == 'numeric':
            resultado[coluna.name] = {
                'ativos': ativos[coluna.name].describe().to_dict(),
                'inativos': inativos[coluna.name].describe().to_dict()
            }
        
        if coluna.type == 'object':
            resultado[coluna.name] = {
                'ativos': ativos[coluna.name].value_counts(normalize=True).to_dict(),
                'inativos': inativos[coluna.name].value_counts(normalize=True).to_dict()
            }

        if coluna.type == 'bool':
            resultado[coluna.name] = {
                'ativos': ativos[coluna.name].value_counts(normalize=True).to_dict(),
                'inativos': inativos[coluna.name].value_counts(normalize=True).to_dict()
            }

    return resultado