import socket, threading


#Define as variáveis de configuração do servidor
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DESCONECTOU"

clientes = []   #Lista que guarda todos os clientes conectados ao servidor

#Inicia o socket do servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

#Função que envia uma mensagem a todos os clientes conectados ao servidor
def SendToAllClients(msg, conn, nome):
    for cliente in clientes:
        if cliente['conexão'] != conn:
            cliente['conexão'].send(f'{nome}: {msg}'.encode(FORMAT))
        else:
            cliente['conexão'].send(f'você: {msg}'.encode(FORMAT))

#Função que lida com as mensagens de cada cliente
def HandleClient(conn, nome):
    print(f'[Nova Conexão] {nome} está conectado')

    connected = True
    while connected:
        msgLength = conn.recv(HEADER).decode(FORMAT)
        if msgLength:   #Caso receba uma mensagem nova
            msgLength = int(msgLength)
            msg = conn.recv(msgLength).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:   #Se for a mensagem de desconexão, o cliente será removido do servidor
                connected = False
            else:   #Para qualquer outra mensagem o servidor irá enviar para todos os clientes
                print(nome + ': ' + msg)
                SendToAllClients(msg, conn, nome)

    index = 0
    for cliente in clientes:
        if cliente['conexão'] == conn:
            break
        index += 1
    print(f'{nome} desconectou com o servidor')
    clientes.pop(index)     #Remove o cliente da lista de clientes
    conn.close()    #Termina a conexão com o cliente

#Função que inicia o servidor e aceita novos clientes
def Start():
    server.listen()
    while True:
        conn, addr = server.accept()
        msgLength = conn.recv(HEADER).decode(FORMAT)
        if msgLength:
            msgLength = int(msgLength)
            nome = conn.recv(msgLength).decode(FORMAT)
        client = {"conexão":conn, "usuario":nome}
        clientes.append(client)
        thread = threading.Thread(target=HandleClient, args=(conn, nome))
        thread.start()
        print(f"[Conexões Ativas] {threading.activeCount() - 1}")

print("[Iniciando] o servidor está iniciando")
Start()