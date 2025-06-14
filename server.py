import socket 
import json
from cryptography.fernet import Fernet

registros = []

# Gerando a chave e salvando as cifras 
chave = Fernet.generate_key()
cipher_suite = Fernet(chave)


s = socket.socket()
s.bind(('localhost', 12345))
s.listen(1)

print("Aguardando conexão...")

conn, addr = s.accept()
print(f"Conectado a {addr}")

# Envia a chave de encript para o cliente.py
conn.send(chave)
print("Chave de encriptação enviada ao cliente")


dados_encriptados = conn.recv(1024)
print(f"Dados encriptados recebidos: {dados_encriptados}")

try:
    # Desencripta os dados
    dados_desencriptados = cipher_suite.decrypt(dados_encriptados)
    dados = json.loads(dados_desencriptados.decode())
    
    registros.append(dados)

    print("\nRegistros enviados do cliente:")
    for r in registros:
        print(f"- Temperatura: {r['temperatura']}°C, Umidade: {r['umidade']}%")


    conn.send(b"Dados recebidos!")

except Exception as e:
    print(f"Erro ao desencriptar ou processar dados: {e}")
    conn.send(b"Erro ao processar os dados encriptados.")

conn.close()
s.close()