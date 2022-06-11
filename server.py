import socket
import threading
import time

SIZE = 1024
FORMAT = "UTF-8"

HOST = socket.gethostbyname(socket.gethostname())
PORT = 6969

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
aliases = []


def broadcast(messege):
    for client in clients:
        client.send(messege)

def handle_client(client):
    while True:
        try:
            message = client.recv(SIZE)
            if "!EXIT" in message.decode(FORMAT):
                client.send("GoodBye :)".encode(FORMAT))
                index = clients.index(client)
                time.sleep(2)
                clients.remove(client)
                client.close()
                alias = aliases[index]
                if len(clients) >= 1:
                    broadcast(f"{alias} as disconnected!".encode(FORMAT))
                aliases.remove(alias)
                print(len(clients))
                break
            else: 
                broadcast(message)
        except ValueError:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            if len(clients) >= 1:
                broadcast(f"{alias} as disconnected!".encode(FORMAT))
            aliases.remove(alias)
            break


def recive():
    while True:
        print("[SERVER] Server is listening....")
        client, address = server.accept()
        print(f"{str(address)} has connected successfully!")
        client.send("Alias?".encode(FORMAT))
        alias = client.recv(SIZE)
        aliases.append(alias)
        clients.append(client)
        print(f"The alias of {address} is {alias}")
        broadcast(f"{alias} has connected to the chat room.".encode(FORMAT))
        client.send("You are connected!".encode(FORMAT))
        thread = threading.Thread(target = handle_client, args=(client,))
        thread.start()

if __name__ == '__main__':
    recive()