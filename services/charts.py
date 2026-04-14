import io 
import base64
import matplotlib.pyplot as plt
import numpy as np

def gerar_grafico_barras(labels, valores_ativos, valores_inativos, titulo):
    fig, ax = plt.subplots(figsize=(10,5))
    
    x = np.arange(len(labels))

    largura = 0.35

    ax.bar(x - largura/2, valores_ativos, largura, label='Ativos', color='#2ecc71')
    ax.bar(x + largura/2, valores_inativos, largura, label='Inativos', color='#e74c3c')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    ax.set_title(titulo)

    buffer = io.BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close(fig)

    return img_str
