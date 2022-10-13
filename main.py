import threading, socket, socketio, asyncio, sys
from misc import *
from time import sleep
import platform
from exceptions import *
__port__ = 58431
__c__ = """
FERRAMENTA FOI DESENVOLVIDA NO INTUITO DE TRANSFERIR ARQUIVOS
EM UMA GRANDE VELOCIDADE; VIA WEBSOCKET.
CASO QUEIRA AJUDAR A CONTINUAR O DESENVOLVIMENTO ENTRE EM CONTATO COMIGO

ATT: Nando Msc
"""
class main:
    def __init__(self) -> None:
        self.port = __port__
        self.ranger = 255
        self.interfaces = allInterfaces()
        self.atualinterface = None
        self.mode:str = None
        os.system("clear" if not platform.system() == "Windows" else "cls")
        print(__c__)
        sleep(1)
        os.system("clear" if not platform.system() == "Windows" else "cls")

    @property
    def aliveClients(self):
        for i in range(0,self.ranger):
            if "ipv4" in self.interfaces.getInterfaces[self.atualinterface]:
                try:
                    s = socket.create_connection(address=("{0}.{1}".format(".".join(self.interfaces.getInterfaces[self.atualinterface]["ipv4"].split(".")[:3]), i), self.port), timeout=.005)
                    yield s
                    s.close()
                except Exception as e:
                    ...
            else:
                raise InterfaceDontHaveIpv4("A interface não possui um ipv4")

    def disconnect(self):
        print("Voce foi desconectado... conecção foi recusada")

    def run(self):
        menu = "Selecione a interface que voce quer\n\n"
        for k,i in self.interfaces.getInterfaces.items():
            menu += "{0}- {1}\n".format(k, i["name"])
        print(menu)
        interfac = input("[0 - {0}] >>> ".format(self.interfaces.getInterfaces.__len__()-1))
        if interfac.replace(" ","").isnumeric():
            if int(interfac) in [*range(self.interfaces.getInterfaces.__len__())]:
                self.atualinterface = int(interfac)
        modes = "Modos disponiveis:\n1 - Receber\n2 - Enviar\n"

        print(modes)
        mode = input("[1 - 2] >>> ")
        if mode.isnumeric():
            match mode:
                case "1":
                    self.mode = "receive"
                case "2":
                    self.mode = "send"
        allow_clients = {

        }
        match self.mode:
            case "send":
                print("[*] procurando clientes online [*]\nUsuarios on-line:\n")
                index_ = 0
                for i in self.aliveClients:
                    allow_clients[index_] = i.getpeername()
                    print("{0}) {1} - on-line".format(index_, i.getpeername()[0]))
                    index_ += 1
                index_ = 0
                if allow_clients.__len__() == 0:
                    print("Nem um usuario online")
                    sleep(1)
                    exit()
                user = input("Selcione um usuario [0 - {0}] >>> ".format(allow_clients.__len__()-1))
                if user.isnumeric():
                    if int(user) in allow_clients:
                        user = allow_clients[int(user)]
                        file = input("local do arquivo >>> ")
                        file.replace("/","\\")
                        sio = socketio.Client()
                        sio.connect("http://{0}:{1}/".format(user[0], user[1]), wait_timeout=60*6,transports=['websocket'], namespaces=['/'])
                        sio.emit("newUser", {"ipv4":self.interfaces.getInterfaces[self.atualinterface]["ipv4"],"name":platform.node()})
                        sio.on('disconnect',self.disconnect)

                        while not sio.connected:
                            pass
                        sleep(5)
                        print("conenctado")
                        if os.path.isfile(file):
                            with open(file, "rb") as r:
                                data = r.readlines()
                                n = 2000
                                l = 0
                                for i in range(0,data.__len__(),n):
                                    l+=len(b''.join(data[i:i+n]))
                                    sio.emit('file',[b''.join(data[i:i+n]),file, len(b''.join(data)), l/1024/1024])
                                    sys.stdout.write("\r{0}.{1} MBs enviados".format(str(l/1024/1024).split(".")[0],str(l/1024/1024).split(".")[-1][:3]))
                                    sys.stdout.flush()
                                    if data[-1] in data[i:i+n]:
                                        sio.disconnect()
                                    sleep(.05)
                                    # def sender(i=i,last=last,data=data,datas=datas,last_= last_, file=file):
                                
                                    # threading.Thread(target=sender,args=(i,last,data,datas,last_,file)).start()
                        print("\npronto")
                        exit()
            case "receive":
                print("\nVoce é reconhecido por: {0}\n".format(self.interfaces.getInterfaces[self.atualinterface]["ipv4"]))
                try:
                    __import__("server.index")
                except Exception as e:
                    print("Já existe uma client em teu dispositivo aberto, esperando conecção.\n", e)
                    exit()
main().run()  
