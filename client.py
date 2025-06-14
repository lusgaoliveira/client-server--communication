import socket
import json
from cryptography.fernet import Fernet

dados = {
    "temperatura": 32,
    "umidade": 12
}

s = socket.socket()
s.connect(("localhost", 12345))

# Pego a chave do server
chave = s.recv(1024)
cipher_suite = Fernet(chave)
print("Chave de encriptação recebida do servidor.")

# Encripta e envia os dados
dados_bytes = json.dumps(dados).encode()
dados_encriptados = cipher_suite.encrypt(dados_bytes)
print(f"Dados encriptados (bytes): {dados_encriptados}")

s.send(dados_encriptados)

# Pegoa a resposta do servidor
print(s.recv(1024).decode())
s.close()
