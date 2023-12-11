import socket
import json

HOST = "localhost"
PORT = 8080
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))


def linha(tamanho=40):
    print("-"*tamanho)


msg = input("Digite seu nome completo: ")
cliente.sendall(msg.encode())

resposta = cliente.recv(1024)
print(f"Resposta do servidor: {resposta.decode()}")


resposta = cliente.recv(1024)
while True:
    escolha = input(resposta.decode()).upper()
    if escolha in "VF":
        break
    print("Escolha inválida. Por favor, digite 'V' para verduras ou 'F' para frutas.")

cliente.sendall(escolha.encode())

resposta = cliente.recv(1024).decode()

produtos_comprados = []
while True:
    linha()
    print(resposta, end="")

    # Pega qual produto o cliente deseja comprar
    id_produto = int(input(
        "Digite qual produto deseja comprar pelo seu ID ou digite 0 para finalizar: "))
    if id_produto == 0:
        # Transforma a lista de produtos comprados em string e envia para o servidor
        produtos_comprados = json.dumps(produtos_comprados)
        cliente.send(produtos_comprados.encode())

        # Recebe o resumo da compra
        resposta = cliente.recv(1024).decode()
        linha()
        print("Logo abaixo está o resumo da sua compra.")
        print(resposta, end="")
        linha(50)
        confirmar_compra = input(
            "Deseja confirmar a compra? Digite S pra sim e N para não: ").upper()
        if confirmar_compra == "S":
            cliente.send(confirmar_compra.encode())
            print("Pagamento confirmado! Volte Sempre! :)")
        break

    quantidade = int(input("Quantas unidades deseja comprar? "))
    produto = {"id": id_produto, "quantidade": quantidade}
    confirmar = input(f"""Então você quer {produto['quantidade']} unidades do produto com id {produto['id']}?
Digite S para confirmar ou N para cancelar a compra: """)

    if confirmar.upper() == "S":
        # Adiciona o produto na lista de compras
        produtos_comprados.append(produto)
        print("Produto adicionado com sucesso a lista de compras!")
    else:
        print("Compra cancelada!")

cliente.close()
