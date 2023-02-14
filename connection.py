import threading
import time
import socket

class TcpClientClass(threading.Thread):
    def __init__(self,addres,port):
        self.running = True
        self.addres = addres
        self.port = port

    def terminate(self):
        self.running = False

    def run(self):
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((self.addres,self.port))
            print('conexao TCP estabelecida')
        except:
            print('falhou em fazer o a conexao TCP como cliente')
            #self.terminate()
        else:
            print('continuando')
            while self.running:
                time.sleep(1) 
                s.send("mensagem enviada para controlar determinado player".encode())
                data = "" 
                while("END" not in data):
                    data = s.recv(1024).decode()
                    print(data)
                break#a logica vem aqui



#Cria a conexao TCP
def connect(port):
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(('127.0.0.1',port))
        print('conexao TCP estabelecida')
        return s
    except:
        print('falhou em fazer o a conexao TCP como cliente')
        return 0
        #self.terminate()
    else:
        print('continuando')


#Da o estado e a recompensa que o agente recebeu
def get_state_reward(s , act):
    s.send(str(act).encode())
    data = "" 
    data_recv = False;
    while(not data_recv):
        data = s.recv(1024).decode()
        try:
            data = eval(data)
            data_recv = True
        except:
            data_recv = False

    #convert the data to decimal int
    estado = data['estado']
    recompensa = data['recompensa']

    return estado, recompensa
