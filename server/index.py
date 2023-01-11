import os, platform,sys
import socketio;
from aiohttp import web;
__port__ = 58431

sio = socketio.AsyncServer(async_mode='aiohttp', binary=True)
app = web.Application(client_max_size=1024**500)
sio.attach(app)

datas = {}
users = {}

@sio.on("connect")
def connect(sid,environ):
    datas[sid] = {"data": None, "filename": "", "recebido":0}
    # y = input("Permitir conecção? s/n >>>")
    # if not y == "s":
    #     return False
    return True

@sio.on("newUser")
async def newuser(sid,data):
    if input("{0} {1} Deseja se conectar S/N >>> ".format(data["ipv4"], data["name"])).lower() in ["n"]:
        await sio.disconnect(sid)
    else:
        users[sid] = data

def save(sid):
    if os.path.exists("./{0}".format(datas[sid]["filename"].split("\\")[-1])):
        with open("./{0}".format(datas[sid]["filename"].split("\\")[-1]), "rb") as r:
            d = r.read()
            with open("./{0}".format(datas[sid]["filename"].split("\\")[-1]), "wb") as w:
                w.write(d+datas[sid]["data"])
                datas[sid]["data"] = b''
    else:
        with open("./{0}".format(datas[sid]["filename"].split("\\")[-1]), "wb") as w:
            w.write(datas[sid]["data"])

@sio.on("file")
async def receiveFile(sid,data):
    if datas[sid]["data"] == None and not datas[sid]["data"] == False:
        print("Recebendo: {0} de {1}. Tamanho: {2}".format(
            data[1].split("\\")[-1],users[sid]["name"], data[2]/1024/1024
        ))
        # if input("Deseja receber: {0} de {1}".format(data[1].split("\\")[-1], users[sid]["name"])).lower() in ["n"]:
        #     await sio.disconnect(sid)
        #     return False
        datas[sid]["data"] = data[0]
        datas[sid]["filename"] = data[1]
    else:
        datas[sid]["data"] = datas[sid]["data"] + data[0] 
    await sio.emit("aaaa","aaaa")

    # if len(data[0]) >= data[2]/2:
    #     save(sid)
    
@sio.on("disconnect")
def disconnect(sid):
    if not datas[sid]["filename"] == '':
        print("Download de: {0} de {1}".format(datas[sid]["filename"].split("\\",)[-1], users[sid]["name"]))
        save(sid)
    del datas[sid]
    if sid in users:
        del users[sid]
if not __name__ == "__main__" or __name__ == "__main__":
    print("Aguradando Coneção")
    web.run_app(app, host='0.0.0.0', port=__port__)  
