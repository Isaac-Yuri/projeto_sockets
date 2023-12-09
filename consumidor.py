import socket
import json

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

resposta = cliente.recv(1024).decode()

produtos_comprados = []
while True:
    print("-"*40)
    print(resposta, end="")

    # Pega qual produto o cliente deseja comprar
    id_produto = input("Digite qual produto deseja comprar pelo seu ID ou digite 0 para sair: ")
    if id_produto == "0":
        break
    quantidade = int(input("Quantas unidades deseja comprar? "))
    produto = {"id": id_produto, "quantidade": quantidade}

    # Adiciona o produto na lista de compras
    produtos_comprados.append(produto)

# Transforma a lista de produtos comprados em string e envia para o servidor
produtos_comprados = json.dumps(produtos_comprados)
cliente.send(produtos_comprados.encode())

cliente.close()
