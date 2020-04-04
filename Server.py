import socket
import sys
import os

PORT = 0
BUF_SIZE = 1024
BASE_ADD = "/Users/zx/Desktop/CSE3461Lab/Receive/"
if len(sys.argv) == 2:
    PORT = sys.argv[1]
    print("\n Server is listening on port :", PORT, "\n")
else:
    print("\n Run the program like:\n python3 Server.py <Port number>\n")
    exit(1)


def upload(connection):
    # Receive filename from client side
    filename = connection.recv(BUF_SIZE)
    if filename:
        filepath = BASE_ADD + filename.decode()
        file = open(filepath, "wb")
        recvdata = connection.recv(BUF_SIZE)
        while recvdata:
            file.write(recvdata)
            recvdata = connection.recv(BUF_SIZE)
        file.close()
    print("\n File has been Transferred successfully \n")


def retrieve(connection):
    filename = connection.recv(BUF_SIZE)
    filepath = BASE_ADD + filename.decode()
    try:
        with open(filepath, 'rb') as file:
            SendData = file.read(BUF_SIZE)
            while SendData:
                connection.send(SendData)
                SendData = file.read(BUF_SIZE)
    except IOError:
        msg = "File not found"
        connection.send(msg.encode())


def authorization(user):
    filepath = BASE_ADD + "Users.txt"
    ret = False
    try:
        with open(filepath, 'r') as file:
            record = file.readline()
            while record:
                if user == record:
                    ret = True
                record = file.readline()
        return ret
    except IOError:
        exit(1)


log=[]
commands = ["Upload", "Retrieve", "Logging", "List", "Quit"]
s = socket.socket()
s.bind(('', int(PORT)))
s.listen()
datatran = socket.socket()
datatran.bind(('', int(PORT)+1))
datatran.listen()
while True:
    conn, addr = s.accept()
    log.append(addr[0])
    msg = "\nHi Client[IP address: " + addr[0] + "], \n ֲֳ**Welcome** \n -Server\n"
    conn.send(msg.encode())
    user = conn.recv(BUF_SIZE)
    auth = authorization(user.decode())
    if auth:
        msg = "Welcome"
        conn.send(msg.encode())
    else:
        while not authorization(user.decode()):
            msg = "User not found"
            conn.send(msg.encode())
            user = conn.recv(BUF_SIZE)
    Comm = conn.recv(BUF_SIZE)
    log.append(Comm.decode())
    args = Comm.decode().split()
    conndata, daddr = datatran.accept()
    while len(args) > 0:
        #print(args)
        while args[0] not in commands or len(args) > 1:
            if args[0] not in commands:
                msg = "Invalid command: " + args[0] + "\n\nCommands:\n  Upload\n  Retrieve\n  Logging\n  List\n  Quit\n"
                conn.send(msg.encode())
                Comm = conn.recv(BUF_SIZE)
                log.append(Comm.decode())
                args = Comm.decode().split()
            if len(args) > 1:
                msg = "Excessive Parameters: " + ''.join(args) + "\n\nCommands:" + args[0] + "\n\nCommands:\n  Upload\n  Retrieve\n  Logging\n  List\n  Quit\n"
                conn.send(msg.encode())
                Comm = conn.recv(BUF_SIZE)
                log.append(Comm.decode())
                args = Comm.decode().split()
        if args[0] == "Upload":
            upload(conndata)
        elif args[0] == "Retrieve":
            retrieve(conndata)
        elif args[0] == "Logging":
            mg = ''.join(log)
            conndata.send(mg.encode())
        elif args[0] == "List":
            msg = os.listdir(BASE_ADD)
            conndata.send(''.join(msg).encode())
        Comm = conn.recv(BUF_SIZE)
        args = Comm.decode().split()
    #conn.close()
    print("\n Server closed the connection \n")

    # Come out from the infinite while loop as the file has been copied from client.
    break
with open(BASE_ADD + "logging.txt", 'w') as file:
    file.write(''.join(log))
s.close()
datatran.close()
