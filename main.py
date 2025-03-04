from openai import OpenAI
from dotenv import load_dotenv
import os

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Criar um cliente da OpenAI utilizando a chave de API
cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Criar uma interação com a OpenAI
resposta = cliente.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "Listar apenas os nomes dos produtos, sem considerar descrição."
        },
        {
            "role": "user",
            "content": "Liste 3 produtos sustentáveis"
        }
    ],
    model="gpt-4"
)

# Imprimir apenas o conteúdo da resposta
print(resposta.choices[0].message.content)