import socket
import threading
import os
import time


SIZE = 1024
FORMAT = "UTF-8"

HOST = socket.gethostbyname(socket.gethostname())
PORT = 6969

alias = input("Choose an alias: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

Is_Dead = False


def client_recive():
    global Is_Dead

    while ~Is_Dead:
        try:
            message = client.recv(SIZE).decode(FORMAT)
            if message == "Alias?":
                client.send(alias.encode(FORMAT))
            else:
                print(message)
        except:
            print("Error")
            Is_Dead = True
            if Is_Dead:
                os.kill(os.getpid(),1)

def client_send():

    global Is_Dead

    while ~Is_Dead:
        message = f"{alias}: {input('')}"
        if "!EXIT" in message:
            client.send(message.encode(FORMAT))
            Is_Dead = True
            if Is_Dead:
                time.sleep(1)
                os.kill(os.getpid(),1)
        else:
            client.send(message.encode(FORMAT))

if __name__ == '__main__':
    recive_thread = threading.Thread(target=client_recive)
    send_thread = threading.Thread(target=client_send)
    recive_thread.start()
    send_thread.start()
   