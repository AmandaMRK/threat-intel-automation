import requests
from datetime import datetime

# --- CONFIGURAÇÕES DO TELEGRAM ---
# (Se preferir, pode colocar suas chaves direto aqui para evitar erros de arquivo .env)
TELEGRAM_BOT_TOKEN = "8803728250:AAEaS5Sui2Z-GHBjwBdpLz8zeUKm-kRl70U"
TELEGRAM_CHAT_ID = "7855365372"

# Lista de serviços/sites que você quer monitorar no suporte
# Pode colocar sites da empresa, sistemas internos ou APIs

SERVICOS_PARA_MONITORAR = [
    {"nome": "Meu GitHub", "url": "https://github.com/AmandaMRK"},
    {"nome": "Meu TryHackMe", "url": "https://tryhackme.com/p/oliveira.limacook"},
    {"nome": "Google", "url": "https://www.google.com"}
]


def enviar_alerta_telegram(mensagem: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID, 
        "text": mensagem, 
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        print("Status Telegram:", response.status_code)
    except Exception as e:
        print(f"[!] Erro ao enviar mensagem para o Telegram: {e}")

if __name__ == "__main__":
    print("--- Iniciando Monitor de Suporte (Uptime Checker) ---")
    
    for servico in SERVICOS_PARA_MONITORAR:
        nome = servico["nome"]
        url_alvo = servico["url"]
        
        print(f"[*] Verificando {nome} ({url_alvo})...")
        
        try:
            # Faz a requisição para testar o site
            resposta = requests.get(url_alvo, timeout=10)
            
            # Se o status code for 200 até 399, consideramos OK
            if 200 <= resposta.status_code < 400:
                print(f"    [OK] {nome} está Online! (Status: {resposta.status_code})")
            else:
                # Servidor respondeu, mas com erro (ex: 500, 404)
                msg_alerta = (
                    f"🚨 *ALERTA DE SUPORTE - SERVIÇO INSTÁVEL*\n\n"
                    f"🖥️ **Serviço:** {nome}\n"
                    f"🔗 **URL:** `{url_alvo}`\n"
                    f"⚠️ **Código HTTP:** `{resposta.status_code}`\n"
                    f"🕒 *{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
                )
                print(f"    [!] ALERTA: {nome} retornou erro {resposta.status_code}!")
                enviar_alerta_telegram(msg_alerta)
                
        except requests.exceptions.RequestException as e:
            # Se cair aqui, o site está totalmente fora do ar (timeout, sem DNS, etc)
            msg_alerta = (
                f"🔥 *ALERTA CRÍTICO - SERVIÇO FORA DO AR*\n\n"
                f"🖥️ **Serviço:** {nome}\n"
                f"🔗 **URL:** `{url_alvo}`\n"
                f"❌ **Erro de Conexão:** O serviço não respondeu.\n"
                f"🕒 *{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
            )
            print(f"    [X] CRÍTICO: {nome} está inacessível!")
            enviar_alerta_telegram(msg_alerta)
