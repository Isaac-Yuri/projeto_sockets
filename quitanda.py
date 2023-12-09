import socket
import threading
from socket import SocketType


def lidar_com_cliente(socket_cliente: SocketType, endereco):
    socket_cliente.send("Bem vindo ao servidor!".encode("utf-8"))
    while True:
        data = socket_cliente.recv(1024)
        if not data:
            break

        data_decoded = data.decode("utf-8")
        nome = data_decoded.split()
        print(f"Nome do consumidor conectado: {data_decoded}")

        socket_cliente.send(f"Recebemos sua mensagem {nome[0]}!".encode("utf-8"))

    socket_cliente.close()
    print(f"Conexão com {endereco} foi encerrada.")


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
