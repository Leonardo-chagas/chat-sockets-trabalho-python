import socket, threading
from tkinter import *
from tkinter import messagebox
from random import randint


#Define as variáveis de configuração do cliente
HEADER = 64
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DESCONECTOU"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
CONNECT = True
NOME = ''

root = Tk()
root.resizable(False, False)

box = Canvas(root, width=600, height=600)
chatBox = Frame(box, bg='blue')
scroll = Scrollbar(box, orient='vertical', command=box.yview)

#Inicia o socket do cliente
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

#Função que aguarda o recebimento de novas mensagens
def Receive():
    global CONNECT, chatBox, box
    while CONNECT:
        mensagem = client.recv(1024).decode(FORMAT)
        if mensagem:
            print(mensagem)
            frame = Frame(chatBox)
            frame.pack(side="top", fill=X)
            label = Label(frame, text=mensagem, justify='left', wraplength=490)
            label.pack(side='left')
            box.update_idletasks()
            box.config(scrollregion=(0,0,0,chatBox.winfo_height()))

#Função que envia mensagens para o servidor
def Send(msg):
    message = msg.encode(FORMAT)
    msgLength = len(message)
    sendLength = str(msgLength).encode(FORMAT)
    sendLength += b' ' * (HEADER - len(sendLength))
    client.send(sendLength)
    client.send(message)

#Função que realiza o login do usuário, e abre a tela do chat
def Login():
    global NOME, chatBox, box, scroll
    NOME = username.get()
    if NOME:
        Send(username.get())
    else:
        NOME = 'usuario' + str(randint(0, 10000))
        Send(NOME)
    loginScreen.destroy()

    box.config(yscrollcommand=scroll.set)
    box.pack(expand=TRUE)
    box.pack_propagate(0)
    box.create_window(0, 0, window=chatBox, anchor=NW)

    #chatBox.grid(row=0, column=0, columnspan=4)
    #chatBox.pack_propagate(0)

    #chatBox.pack(expand=TRUE, fill=Y)

    scroll.pack(side=RIGHT, fill=Y, expand=FALSE)

    userArea = Frame(root, width=300, height=30)
    userArea.pack()

    textMessage = Entry(userArea, width=80)
    textMessage.grid(row=0, column=0)
    textMessage.grid_columnconfigure(0, weight=3)

    sendButton = Button(userArea, command= lambda: Send(textMessage.get()), width=10, text='Enviar')
    sendButton.grid(row=0, column=1)
    sendButton.grid_columnconfigure(1, weight=1)

    thread = threading.Thread(target=Receive)   #Inicia a thread que aguarda o recebimento de mensagens
    thread.start()

#função que desconecta o usuário do servidor quando ele fechar a janela
def Close():
    global CONNECT, NOME
    if messagebox.askokcancel('Sair', 'Você deseja sair do chat?'):
        CONNECT = False
        if NOME:
            Send(DISCONNECT_MESSAGE)
        root.destroy()

#cria a tela de login, com o widget de entrada e o botão de realização de login
loginScreen = Frame(root)
loginScreen.pack()

nome = Label(loginScreen, text='Nome: ')
nome.grid(row=0, column=0)
nome.grid_rowconfigure(0, weight=1)
nome.grid_columnconfigure(0, weight=1)

username = Entry(loginScreen)
username.grid(row=0, column=1)
username.grid_columnconfigure(1, weight=2)
username.grid_rowconfigure(0, weight=2)

loginButton = Button(loginScreen, text='Fazer Login', command=Login, width=17)
loginButton.grid(row=2, column=1)
loginButton.grid_columnconfigure(1, weight=1)
loginButton.grid_rowconfigure(2, weight=1)


root.protocol('WM_DELETE_WINDOW', Close)
root.mainloop()