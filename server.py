import socket
import threading
host="127.0.0.1"
port=55556
SERVER="192.168.137.233"
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

clients=[]
nicknames=[]

def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            clients.remove(client)


def handle(client):
    while True:
        try:
            msg=message = client.recv(1024)
            if msg.decode('ascii').startswith('KICK'):
                if nicknames[clients.index(client)]=='admin':
                    name_to_kick=msg.decode('ascii')[5:]
                    kick_user(name_to_kick)
                else:
                    client.send('command was refuse'.encode('ascii'))
            elif msg.decode('ascii').startswith('BAN'):
                if nicknames[clients.index(client)]=='admin':
                    name_to_ban=msg.decode('ascii')[4:]
                    kick_user(name_to_ban)
                    with open('bans.txt','a') as f:
                        f.write(f'{name_to_ban}\n')
                    print(f'{name_to_ban} was banned')
                else:
                    client.send('command was refuse'.encode('ascii'))
            else:
                broadcast(message)
        except:
            # Remove client safely if errror
            if client in clients:
                index = clients.index(client)
                nickname = nicknames[index]
                clients.remove(client)
                nicknames.remove(nickname)
                broadcast(f'{nickname} left the chat'.encode('ascii'))
            client.close()  # close the socket
            return  

def recive():
    while True:
        client,address= server.accept()
        print(f'connected with {str(address)}')
        client.send('NICK'.encode('ascii'))
        nickname= client.recv(1024).decode('ascii')

        with open('bans.txt','r') as f :
            bans=f.readlines()
        if nickname+'\n' in bans:
            client.send('BAN'.encode('ascii'))
            client.close()
            continue
        
        #Password
        if nickname=='admin':
            client.send('PASS'.encode('ascii'))
            password= client.recv(1024).decode('ascii')
            if password != 'mini_project':
                client.send('REFUSE'.encode('ascii'))
                client.close()
                continue
        nicknames.append(nickname)
        clients.append(client)
        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} join the chat'.encode('ascii'))
        client.send('Connected to the server'.encode('ascii'))

        thread=threading.Thread(target=handle,args=(client,))
        thread.start()

def kick_user(name):
    if name in nicknames:
        name_index=nicknames.index(name)
        client_to_kick=clients[name_index]
        #clients.remove(client_to_kick)
        client_to_kick.send('you are kicked by an admin!'.encode('ascii'))
        clients.remove(client_to_kick)
        client_to_kick.close()
        nicknames.remove(name)
        broadcast(f'{name} is kicked by an admin!'.encode('ascii'))
recive()
print('server is running!')

    