from groq import Groq
from settings import settings
from processor import filtro_analise_colunas

def criar_prompt(resultado: dict)-> dict:
    prompt = "Analise os seguintes dados comparativos entre clientes ativos e inativos:\n\n"
    
    for coluna, dados in resultado.items():
        prompt += f"Coluna '{coluna}':\n"
        prompt += f"  Ativos: {dados['ativos']}\n"
        prompt += f"  Inativos: {dados['inativos']}\n\n"
    
    prompt += (
        "Com base nesses dados:\n"
        "1. Identifique os principais padrões que diferenciam ativos de inativos\n"
        "2. Aponte quais variáveis têm maior impacto na inatividade\n"
        "3. Sugira ações concretas para reduzir a perda de clientes\n"
        "4. Se possível, indique segmentos de risco que merecem atenção imediata"
    )
    
    return prompt

def gerar_resposta(dados: dict, prompt: dict)-> str:
    client = Groq(api_key=settings.ai_api_key)

    request = client.chat.completions.create(
        model = 'llama-3.3-70b-versatile',
        messages=['role': 'user', 
                'content': prompt]
    )

