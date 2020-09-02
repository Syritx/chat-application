import socket
import threading as thr

# creating server
ip = socket.gethostbyname(socket.gethostname())
port = 5050

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip,port))

clients = set()
clients_lock = thr.Lock()

# multithreading
def handle_client(client,addr):
    print("connection from " + str(addr))
    with clients_lock:
        clients.add(client)

    connected = True

    disconnected_message = "DISCONNECTED_FROM_CHAT_APP"
    byte = 1024

    while connected:
        message_len = client.recv(byte).decode("utf-8")

        if message_len != None:

            # receiving message from the client
            message_len = int(message_len)
            message = client.recv(message_len).decode("utf-8")

            if message == disconnected_message:
                print("disconnected")
                connected = False
                break
            else:
                print("[" + str(addr) + "]: " + message)

                # sending a client message to other clients
                with clients_lock:
                    for c in clients:

                        if (c != client):
                            c.sendall(message+"\n")
                            print("sent")
    # removing clients
    with clients_lock:
        clients.remove(client)
        client.close()

# accepting clients
def start_server():
    server.listen(10)

    while True:
        client, addr = server.accept()

        thread = thr.Thread(target=handle_client,args=(client,addr))
        thread.start()

start_server()
