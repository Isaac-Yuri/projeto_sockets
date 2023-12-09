import socket

HOST = "localhost"
PORT = 8080
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))

msg = input("Digite seu nome completo: ")
cliente.sendall(msg.encode())

resposta = cliente.recv(1024)
print(f"Resposta do servidor: {resposta.decode()}")


resposta = cliente.recv(1024)
while True:
    escolha = input(resposta.decode())
    if escolha.upper() in "VF":
        break
    print("Escolha inválida. Por favor, digite 'V' para verduras ou 'F' para frutas.")

cliente.sendall(escolha.encode())

cliente.close()