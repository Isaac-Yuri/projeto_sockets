import socket

HOST = "localhost"
PORT = 8080

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cliente.connect((HOST, PORT))

msg = input("Digite uma mensagem a ser enviada para o servidor: ")

cliente.sendall(msg.encode())

resposta = cliente.recv(1024)

print(f"Resposta do servidor: {resposta.decode()}")

resposta = cliente.recv(1024)

print(resposta.decode())

cliente.close()