import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

SERVICOS_PARA_MONITORAR = [
    {"nome": "Meu GitHub", "url": "https://github.com/AmandaMRK"},
    {"nome": "Google", "url": "https://www.google.com"},
    {"nome": "Meu TryHackMe", "url": "https://tryhackme.com/p/oliveira.limacook"},
    {"nome": "Simulador de Queda (Erro 500)", "url": "https://httpbin.org/status/500"}
]

def enviar_alerta_telegram(mensagem):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Erro: Variáveis do Telegram não configuradas.")
        return
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensagem,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"Status Telegram: {response.status_code}")
    except Exception as e:
        print(f"Erro ao enviar mensagem para o Telegram: {e}")

def monitorar_servicos():
    print("\n--- Iniciando Monitor de Suporte (Uptime Checker) ---")
    for servico in SERVICOS_PARA_MONITORAR:
        nome = servico["nome"]
        url = servico["url"]
        
        try:
            resposta = requests.get(url, timeout=10)
            
            if resposta.status_code != 200:
                print(f"[!] ALERTA: {nome} retornou erro {resposta.status_code}!")
                mensagem = (
                    f"🚨 *ALERTA DE SUPORTE - SERVIÇO INSTÁVEL*\n\n"
                    f"💻 *Serviço:* {nome}\n"
                    f"🔗 *URL:* {url}\n"
                    f"⚠️ *Código HTTP:* {resposta.status_code}"
                )
                enviar_alerta_telegram(mensagem)
            else:
                print(f"[OK] {nome} está Online! (Status: 200)")
                
        except requests.exceptions.RequestException as e:
            print(f"[X] ERRO de Conexão com {nome}: {e}")
            mensagem = (
                f"🚨 *ALERTA DE SUPORTE - FALHA DE CONEXÃO*\n\n"
                f"💻 *Serviço:* {nome}\n"
                f"🔗 *URL:* {url}\n"
                f"❌ *Erro:* O serviço ficou inacessível."
            )
            enviar_alerta_telegram(mensagem)

if __name__ == "__main__":
    print("Bot de monitoramento iniciado na nuvem...")
    while True:
        monitorar_servicos()
        time.sleep(300)
