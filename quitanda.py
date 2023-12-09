import socket
import threading
import json
from socket import SocketType


def lidar_com_cliente(client_socket: SocketType, endereco):
    client_socket.send("Bem vindo ao servidor!".encode("utf-8"))
    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        data_decoded = data.decode("utf-8")
        nome = data_decoded.split()
        print(f"Nome do consumidor conectado: {data_decoded}")

        client_socket.send(f"Você quer comprar frutas ou verduras {nome[0]}? \nDigite V para verduras e F para frutas >>> ".encode("utf-8"))

        # Recebe que tipo de produto o cliente quer comprar
        data = client_socket.recv(1024).decode()

        menu = f"PRODUTO  | PREÇO | ID |\n"
        # Se data for V manda o menu com as verduras se for F manda o menu com as frutas
        if data == "V":
            verduras = [["Agrião   ", 3], ["Brócolis ", 2.5],
                        ["Coentro  ", 2], ["Espinafre", 4]]
            id_counter = 0
            for verdura in verduras:
                id_counter += 1
                verdura.append(id_counter)
                menu += f"{verdura[0]}| R${verdura[1]:.1f} | {verdura[2]}  |\n"

        elif data == "F":
            frutas = [["Maça     ", 1.8], ["Laranja  ", 2],
                      ["Uva      ", 1.5], ["Morango  ", 3]]
            id_counter = 0
            for fruta in frutas:
                id_counter += 1
                fruta.append(id_counter)
                menu += f"{fruta[0]}| R${fruta[1]:.1f} | {fruta[2]}  |\n"

        # Envia o menu de produtos para o cliente
        client_socket.send(menu.encode())

        # Pega a lista de produtos que o cliente deseja comprar
        lista_produtos = client_socket.recv(1024).decode()
        lista_produtos: dict = json.loads(lista_produtos)
        

        # Mensagem de encerramento da conexão
        print(f"Conexão com {nome[0]} foi encerrada.")

    client_socket.close()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
endereco = ("localhost", 8080)
server_socket.bind(endereco)
server_socket.listen(5)

print(f"Servidor escutando em {endereco[0]}:{endereco[1]}")

while True:
    try:
        client_socket, address = server_socket.accept()
        print(f"Conexão estabelecida com {address[0]}:{address[1]}")

        thread_cliente = threading.Thread(
            target=lidar_com_cliente, args=(client_socket, address))
        thread_cliente.start()
    except KeyboardInterrupt:
        print("Servidor Encerrado!")
        break

server_socket.close()
