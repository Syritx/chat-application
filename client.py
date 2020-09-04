import socket
import signal

# connecting client
ip = socket.gethostbyname(socket.gethostname())
port = 5050

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip,port))

def handler(signum, frame):
    client.send("DISCONNECTED_FROM_CHAT_APP")

signal.signal(signal.SIGHUP, handler)

def send_message(message):
    
    # sending messages to the server
    msg = message.encode("utf-8")
    msg_len = len(msg)

    send_len = str(msg_len).encode("utf-8")
    send_len += b' ' * (1024 - len(send_len))

    client.send(send_len)
    client.send(msg)
    return

while 1:
    msg = input("[YOU]: ")
    send_message(msg)

    print(client.recv(2048).decode("utf-8"))
