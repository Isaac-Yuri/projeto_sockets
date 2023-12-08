import socket

HOST = 'localhost'
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen(5)

print(f"Servidor escutando em {HOST}:{PORT}")

while True:
    client_socket, addr = server_socket.accept()
    
    print(f"Conexão recebida de {addr[0]}:{addr[1]}")

    data = client_socket.recv(1024)
    if not data:
        break
    
    print(f"Mensagem recebida: {data.decode()}")

    client_socket.sendall("Mensagem recebida pelo servidor".encode())

    client_socket.close()

server_socket.close()
