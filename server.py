import socket
import threading
import time

#Com esse comando o socket escolhe por padrão
#Você também pode colocar uma string como IP
SERVER_IP = socket.gethostbyname(socket.gethostname())
PORT = 5050

#É usado para fazer o server bind ele recebe o IP e porta
ADDR = (SERVER_IP, PORT)
#Esse é o formato que a mensagem será codificada
FORMATO = 'utf-8'

#AF_INET é a classe do socket
#SOCK_STREAM é o tipo de entrada e saída
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

conexoes = []
mensagens = []

#4 funções principais
#Manda para uma pessoa
def enviar_mensagem_individual(conexao):
    print(f"[ENVIANDO] Envinando mensagens para {conexao['addr']}")
    for i in range(conexao['last'], len(mensagens)):
        mensagem_de_envio = 'msg=' + mensagens[i]
        conexao['conn'].send(mensagem_de_envio.encode())
        conexao['last'] = i + 1
        #Para não sobrecarregar mandando mais rápido do que o pc recebe
        time.sleep(0.2)
#Manda para todas as conexões
def enviar_mensagem_todos():
    global conexoes

    for conexao in conexoes:
        enviar_mensagem_individual(conexao)

"""
1 vez que o usuário entra ele manda o nome
nome=...
E as mensagens vem:
msg=
"""

def handle_clients(conn, addr):
    print(f"[NOVA CONEXÂO] Um novo usuário se conectou pelo endereço {addr}")
    
    global conexoes
    global mensagens

    nome = False

    while(True):
        msg = conn.recv(1024).decode(FORMATO)
        if(msg): #checa se a mensagem não é nula
            if(msg.startswith('nome=')):
                mensagem_separada=msg.split('=')
                nome = mensagem_separada[1]

                mapa = {
                    'conn': conn,
                    'addr': addr,
                    'nome': nome,
                    'last': 0
                }

                #Adiciona o usuário à lista de conexões do grupo
                conexoes.append(mapa)

                enviar_mensagem_individual(mapa)
            elif(msg.startswith("msg=")):
                mensagem_separada = msg.split("=")
                mensagem = nome + "=" + mensagem_separada[1]
                
                mensagens.append(mensagem)

                enviar_mensagem_todos()

'127.0.1.1'

def start():
    print("[INICIANDO] Iniciando Socket")
    print(f"Endereço: {ADDR}")

    
    #Põe o servidor para ouvir a requisição
    server.listen()
    while(True):
        #Aceita a entrada de um cliente
        #Ele fica esperando um cliente mandar algo
        conn, addr = server.accept()
        #Cria uma thread para um novo usuário quando ele entra
        #em seguida ela é iniciada
        thread = threading.Thread(target=handle_clients, args=(conn, addr))
        thread.start()

start()