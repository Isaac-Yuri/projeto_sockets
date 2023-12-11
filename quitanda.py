import socket
import threading
import json
from socket import SocketType


def criar_menu(produtos: list) -> str:
    menu = f"PRODUTO  | PREÇO | ID |\n"
    id_counter = 0
    for produto in produtos:
        id_counter += 1
        produto.append(id_counter)
        menu += f"{produto[0]}| R${produto[1]:.1f} | {produto[2]}  |\n"
    return menu


def montar_resumo_compra(produtos_comprados):
    resumo = f"PRODUTO  | PREÇO | QUANTIDADE |  TOTAL  | \n"
    total = 0
    for produto in produtos_comprados:
        preco_total = produto[1] * produto[2]
        total += preco_total
        # Os ifs abaixo são para questão de layout do resumo
        if produto[2] >= 10:
            if preco_total < 10:
                resumo += f"{produto[0]}| R${produto[1]                                             :.1f} |     {produto[2]}     |  R${preco_total:.1f}  |\n"
            else:
                resumo += f"{produto[0]}| R${produto[1]                                             :.1f} |     {produto[2]}     |  R${preco_total:.1f} |\n"
        else:
            if preco_total < 10:
                resumo += f"{produto[0]}| R${produto[1]:.1f} |     {
                    produto[2]}      |  R${preco_total:.1f}  |\n"
            else:
                resumo += f"{produto[0]}| R${produto[1]                                             :.1f} |     {produto[2]}      |  R${preco_total:.1f} |\n"
    resumo += f"O valor total da compra foi de R${total}\n"
    return resumo


def somar_ao_caixa(caixa: int, produtos_comprados):
    total = 0
    for produto in produtos_comprados:
        preco_total = produto[1] * produto[2]
        total += preco_total
    caixa += total


def msg_de_compra(produtos_comprados, nome_do_consumidor):
    total = 0
    for produto in produtos_comprados:
        preco_total = produto[1] * produto[2]
        total += preco_total
    return f"+R${total} de {nome_do_consumidor}"


server_running = True
caixa = 0


def lidar_com_cliente(client_socket: SocketType, endereco):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        data_decoded = data.decode("utf-8")
        nome = data_decoded.split()
        print(f"Nome do consumidor conectado: {data_decoded}")

        client_socket.send(f"Você quer comprar frutas ou verduras {nome[0]}? \nDigite V para verduras e F para frutas >>> ".encode())

        # Recebe que tipo de produto o cliente quer comprar
        data = client_socket.recv(1024).decode()

        produtos = []
        menu = ""
        global caixa 

        # Se data for V cria o menu com as verduras se for F cria o menu com as frutas
        if data == "V":
            verduras = [["Agrião   ", 3], ["Brócolis ", 2.5],
                        ["Coentro  ", 2], ["Espinafre", 4]]
            menu = criar_menu(verduras)
            produtos = verduras

        elif data == "F":
            frutas = [["Maça     ", 1.8], ["Laranja  ", 2],
                      ["Uva      ", 1.5], ["Morango  ", 3]]
            menu = criar_menu(frutas)
            produtos = frutas

        # Envia o menu de produtos para o cliente
        client_socket.send(menu.encode())

        # Pega a lista de produtos que o cliente deseja comprar
        carrinho_compras_consumidor = client_socket.recv(1024).decode()
        carrinho_compras_consumidor: list = json.loads(
            carrinho_compras_consumidor)

        produtos_comprados = []
        for produto in produtos:
            id_produto = produto[2]
            for produto_no_carrinho in carrinho_compras_consumidor:
                if id_produto == produto_no_carrinho["id"]:
                    # Produto comprado e a quantidade do mesmo respectivamente
                    produto_comprado = [produto[0], produto[1],
                                        produto_no_carrinho["quantidade"]]
                    produtos_comprados.append(produto_comprado)

        # Envia o resumo da compra
        resumo_da_compra = montar_resumo_compra(produtos_comprados)
        client_socket.send(resumo_da_compra.encode())

        # Recebe a confirmação de compra
        data = client_socket.recv(1024).decode()
        if data == "S":
            # Soma o valor da compra ao caixa
            somar_ao_caixa(caixa, produtos_comprados)
            print(msg_de_compra(produtos_comprados, nome[0]))

        # Mensagem de encerramento da conexão
        print(f"Conexão com {nome[0]} foi encerrada.")

    client_socket.close()


def aceitar_conexoes(server_socket):
    global server_running
    while server_running:
        try:
            client_socket, address = server_socket.accept()
            print(f"Conexão estabelecida com {address[0]}:{address[1]}")

            thread_cliente = threading.Thread(
                target=lidar_com_cliente, args=(client_socket, address), daemon=True)
            thread_cliente.start()
        except OSError:
            break


def iniciar_servidor():
    global server_running
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    endereco = ("localhost", 8080)
    server_socket.bind(endereco)
    server_socket.listen(5)

    print(f"Servidor escutando em {endereco[0]}:{endereco[1]}")

    # Inicia a thread para aceitar conexões
    thread_aceitar_conexoes = threading.Thread(
        target=aceitar_conexoes, args=(server_socket,))
    thread_aceitar_conexoes.start()

    try:
        while server_running:
            pass
    except KeyboardInterrupt:
        print("Servidor Encerrando...")
    finally:
        server_running = False
        server_socket.close()


if __name__ == "__main__":
    iniciar_servidor()
