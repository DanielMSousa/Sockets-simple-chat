import socket
import threading
import time

SERVER_IP = '127.0.1.1'
PORT = 5050
ADDR = (SERVER_IP, PORT)
FORMATO = 'utf-8'

#cliente e servidor se conectam basicamente mesma forma.
#porém ao invés de bind usa connect
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def handle_mensagens():
    while True:
        #No decode você não põe o formato, só no encode.
        msg = client.recv(1024).decode()
        mensagem = msg.split('=')
        print(mensagem[1]+': '+mensagem[2])

def enviar(mensagem):
    client.send(mensagem.encode(FORMATO))

def enviar_mensagem():
    mensagem = input()
    enviar("msg="+mensagem)

def enviar_nome():
    nome = input('Digite seu nome: ')
    enviar("nome="+nome)

def iniciar_envio():
    enviar_nome()
    while True:
        enviar_mensagem()

def iniciar():
    thread1 = threading.Thread(target=handle_mensagens)
    thread2 = threading.Thread(target=iniciar_envio)
    thread1.start()
    thread2.start()

iniciar()