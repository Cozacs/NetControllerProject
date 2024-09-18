import subprocess
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import sys

EMAIL_HOST = 'smtp.titan.email' # Email Host
EMAIL_PORT = 587 # Port
EMAIL_USER = '' # Email Config
EMAIL_PASS = '' # Password Config
EMAIL_TO = sys.argv[1] 

historico_erro = []

def enviar_email(mensagem):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_TO
    msg['Subject'] = 'Status de Conexão de Rede'

    msg.attach(MIMEText(mensagem, 'plain'))

    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASS)
    text = msg.as_string()
    server.sendmail(EMAIL_USER, EMAIL_TO, text)
    server.quit()

def verificar_ping(host):
    comando = ["ping", "-n", "4", host]
    resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if resultado.returncode == 0:
        print(f"Ping bem-sucedido.")
        if historico_erro:
            hora = datetime.now().strftime("%H:%M %d/%m/%y")
            enviar_email(f"A sua internet voltou {hora}, ela ficou fora do ar por {len(historico_erro)} minutos.")
            historico_erro.clear() 
            print(f"O e-mail foi enviado com sucesso e o seu historico de erros está atualmente com a contagem em {len(historico_erro)}.")
    else:
        print(f"Falha ao pingar {host}.")
        historico_erro.append(f"Falha em {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Erro registrado. Histórico: {len(historico_erro)} falhas.")
if __name__ == "__main__":
    try:
        while True:
            verificar_ping("google.com")
            time.sleep(60)  
    except KeyboardInterrupt:
        print("Monitoramento interrompido pelo usuário.")
