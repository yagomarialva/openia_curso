from openai import OpenAI
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

# Verificar se a chave da API foi carregada
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Chave da API não encontrada. Verifique seu arquivo .env")

# Criar o cliente da OpenAI
cliente = OpenAI(api_key=api_key)

# Definir o modelo
modelo = "gpt-4"

def categoriza_produto(nome_produto, lista_categorias_possiveis):
    # Criar a prompt formatada corretamente
    categorias_formatadas = ", ".join(lista_categorias_possiveis.split(","))
    prompt_sistema = f"""
        Você é um categorizador de produtos.
        Você deve assumir as categorias presentes na lista abaixo.

        # Lista de Categorias Válidas
        {categorias_formatadas}

        # Formato da Saída
        Produto: Nome do Produto
        Categoria: apresente a categoria do produto

        # Exemplo de Saída
        Produto: Escova elétrica com recarga solar
        Categoria: Eletrônicos Verdes
    """

    try:
        # Criar interação com a OpenAI
        resposta = cliente.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": prompt_sistema
                },
                {
                    "role": "user",
                    "content": f"Produto: {nome_produto}"
                }
            ],
            temperature=0.5,
            model=modelo,
            max_tokens=200,
            n=1  # Queremos apenas uma resposta
        )

        # Garantir que há uma resposta válida antes de acessar choices[0]
        if resposta.choices and len(resposta.choices) > 0:
            return resposta.choices[0].message.content.strip()
        else:
            return "Erro: A API não retornou uma resposta válida."

    except Exception as e:
        return f"Erro ao chamar a API: {str(e)}"

# Solicitar categorias válidas
categorias_validas = input("Informe as categorias válidas, separando por vírgula: ")

while True:
    nome_produto = input("\nDigite o nome de um produto (ou 'sair' para encerrar): ").strip()

    if nome_produto.lower() == "sair":
        print("Encerrando o programa.")
        break

    # Chamar a função de categorização
    texto_resposta = categoriza_produto(nome_produto, categorias_validas)

    # Exibir a resposta categorizada
    print("\nResposta do modelo:\n", texto_resposta)
