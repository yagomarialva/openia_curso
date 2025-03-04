from openai import OpenAI
from dotenv import load_dotenv
import os
import tiktoken

# Carregar variáveis de ambiente
load_dotenv()

# Criar cliente da OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Modelo inicial
modelo_padrao = "gpt-4"
modelo_alternativo = "gpt-4-1106-preview"
tamanho_esperado_saida = 2048

# Inicializar codificador de tokens
codificador = tiktoken.encoding_for_model(modelo_padrao)

def carrega(nome_do_arquivo):
    """ Carrega um arquivo e retorna seu conteúdo ou uma string vazia em caso de erro. """
    try:
        with open(nome_do_arquivo, "r", encoding="utf-8") as arquivo:
            return arquivo.read()
    except IOError as e:
        print(f"Erro ao carregar '{nome_do_arquivo}': {e}")
        return ""  # Retorna uma string vazia se houver erro

def escolhe_modelo(prompt_sistema, prompt_usuario):
    """ Escolhe o modelo baseado no número de tokens. """
    lista_de_tokens = codificador.encode(prompt_sistema + prompt_usuario)
    numero_de_tokens = len(lista_de_tokens)
    
    print(f"Número de tokens na entrada: {numero_de_tokens}")

    if numero_de_tokens >= 4096 - tamanho_esperado_saida:
        return modelo_alternativo
    return modelo_padrao

# Definir prompt do sistema
prompt_sistema = """
Identifique o perfil de compra para cada cliente a seguir.

O formato de saída deve ser:

cliente - descreva o perfil do cliente em 3 palavras
"""

# Carregar dados do usuário
caminho_arquivo = "dados/lista_de_compras_100_clientes.csv"
prompt_usuario = carrega(caminho_arquivo)

# Escolher modelo com base nos tokens
modelo = escolhe_modelo(prompt_sistema, prompt_usuario)
print(f"Modelo escolhido: {modelo}")

# Criar lista de mensagens
lista_mensagens = [
    {"role": "system", "content": prompt_sistema},
    {"role": "user", "content": prompt_usuario}
]

try:
    # Fazer a requisição para a OpenAI
    resposta = client.chat.completions.create(
        messages=lista_mensagens,
        model=modelo
    )

    # Exibir resposta
    print("\nResposta da IA:")
    print(resposta.choices[0].message.content)

except Exception as e:
    print(f"Erro ao chamar a OpenAI: {e}")
