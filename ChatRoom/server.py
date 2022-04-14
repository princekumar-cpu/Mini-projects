import socket
import  threading
PORT = 50001
HOST = socket.gethostbyname((socket.gethostname())) # This will create host address(ip address like 192.168.43.226)
ADDRESS = ( HOST, PORT)

FORMAT = "UTF-8"
clients = []
server = []
names = []
# Create a socket for the server where AF_INET is the type of address (will return )
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

def start_chat():
    print("Server is Working on :"+ HOST)

    server.listen()
    while True:
        connection, addr = server.accept()
        connection.send("NAME".encode(FORMAT))

        name = connection.recv(1025).decode(FORMAT)
        names.append(name)

        clients.append(connection)
        print("Name is : {}".format(name))

        broadcastMessage(f"{name} has joined the group".encode(FORMAT))

        connection.send("Connection Successful".encode(FORMAT))
        thread = threading.Thread(target=receive, args=(connection,addr))
        thread.start()
        print(f"active connection {threading.active_count()- 1}")
def receive(connection,addr):
    print(f"New connection {addr}")
    connected = True
    while connected:
        message = connection.recv(1025)
        broadcastMessage(message)
    connection.close()

def broadcastMessage(message):
    for client in clients:
        client.send(message)
start_chat()
