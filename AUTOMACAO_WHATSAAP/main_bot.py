from flask import Flask, request
import requests

app = Flask(__name__)

# Substitua com os seus dados
TOKEN = '26D0211A46019D04D7539F73'
INSTANCE_ID = '3E4DE9D8A56F60588FB45E8072250E75'
BASE_URL = f'https://api.z-api.io/instances/{INSTANCE_ID}/token/{TOKEN}'

# Função para enviar mensagem
def enviar_mensagem(numero, mensagem):
    url = f'https://api.z-api.io/instances/{INSTANCE_ID}/send-text'

    payload = {
        "phone": str(numero),  # Certifique-se que é string
        "message": mensagem
    }

    headers = {
        "Content-Type": "application/json",
        "Client-Token": TOKEN
    }

    response = requests.post(url, json=payload, headers=headers)

    print("📤 Enviando mensagem para:", numero)
    print("📦 Payload:", payload)
    print("🔁 Status Code:", response.status_code)
    print("🔄 Resposta:", response.text)

    response.raise_for_status()


@app.route('/webhook', methods=['POST'])
def receber_mensagem():
    dados = request.json
    print("📨 Webhook chamado!")
    print("🔎 Dados recebidos:", dados)

    # Verifica se há 'text' e 'message'
    if 'text' in dados and 'message' in dados['text']:
        mensagem = dados['text']['message']
        numero = dados['phone']

        if mensagem == "1":
            enviar_mensagem(numero, "🔧 Valores dos pneus:\n- Aro 13: R$200\n- Aro 14: R$250\n- Aro 15: R$300")
        elif mensagem == "2":
            enviar_mensagem(numero, "🛠️ Vamos agendar sua avaliação. Qual o modelo do carro?")
        elif mensagem == "3":
            enviar_mensagem(numero, "📞 Um atendente irá te chamar em instantes.")
        else:
            enviar_mensagem(numero,
                "👋 Olá! Escolha uma opção:\n1️⃣ Ver valores de pneus\n2️⃣ Fazer avaliação de problemas no carro\n3️⃣ Falar com atendente")
    else:
        print("⚠️ Ignorado: Payload sem 'text' ou 'message'")

    return "OK", 200


if __name__ == '__main__':
    app.run(port=5000)
