import socket
import threading

nickname= input("Enter your nickname: ")
if nickname=='admin':
    password=input("Enter the admin password:")

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('127.0.0.1',55556))

stop_thread=False

def recive():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message=client.recv(1024).decode('ascii')
            if message=='NICK':
                client.send(nickname.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')
                if next_message =='PASS':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii')=='REFUSE':
                        print("Connection denied! Wrong Password")
                        stop_thread=True
                elif next_message=='BAN':
                    print('Connection closed due to Ban!')
                    client.close()
                    stop_thread=True
            else:
                print(message)
        except:
            print("Error occurred!")
            client.close()
            break
    
def write():
    while True:
        if stop_thread:
            break
        message=f'{nickname}:{input("")}'
        if message[len(nickname)+2:].startswith('/'):
                if nickname=='admin':
                    if message[len(nickname)+1:].startswith('/kick'):
                        client.send(f'KICK {(message[len(nickname)+1+5:])}'.encode('ascii'))
                    elif message[len(nickname)+1:].startswith('/ban'):
                        client.send(f'BAN {(message[len(nickname)+1+4:])}'.encode('ascii'))
                else:
                    print('Command can only executed by the admin')
        else:
            client.send(message.encode('ascii'))

recive_thread=threading.Thread(target=recive)
recive_thread.start()

write_thread= threading.Thread(target=write)
write_thread.start()

