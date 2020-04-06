import socket
import sys
import time

BUF_SIZE = 1024
BASE_ADD = ""

if len(sys.argv) == 3:
    ServerIp = sys.argv[1]
    ServerPort = sys.argv[2]
else:
    print("\n  Run the program like:\n python3 Client.py < serverip address > <Port number>\n")
    exit(1)


def upload(soc):
    filename = input("\nPlease enter file name:\n")
    soc.send(filename.encode())
    filename = BASE_ADD + filename
    with open(filename, "rb") as file:
        soc.sendfile(file,0)
    print("\n File has been Transferred successfully \n")


def retrieve(soc):
    filename = input("\nPlease enter file name you want to retrieve:\n")
    soc.send(filename.encode())
    if filename:
        filepath = BASE_ADD + filename
        with open(filepath, "wb") as file:
            recvdata = soc.recv(BUF_SIZE)
            while recvdata:
                file.write(recvdata)
                recvdata = soc.recv(BUF_SIZE)
    print("\n File has been retrieved successfully \n")



commands = ["Upload", "Retrieve", "Logging", "List", "Quit"]
s = socket.socket()
s.connect((ServerIp, int(ServerPort)))
print(s.recv(BUF_SIZE).decode())
user = input("Please input Username and password: ")
s.send(user.encode())
info = s.recv(BUF_SIZE)
if info.decode() == "\n  Welcome":
    print(info.decode())
else:
    while info.decode() == "User not found":
        print(info.decode())
        user = input("Please input Username and password: ")
        s.send(user.encode())
        info = s.recv(BUF_SIZE)
    print(info.decode())
while True:
    Command = input("\nPlease enter command:\n Upload, Retrieve, List, Logging, Quit\nCommand:")
    s.send(Command.encode())
    while Command:
        if Command in commands:
            break
        Data = s.recv(BUF_SIZE)
        print(Data.decode())
        Command = input("\nPlease enter command:\n Upload, Retrieve, List, Logging, Quit\nCommand:")
        s.send(Command.encode())
    if Command == "Upload":
        time.sleep(1)
        soc = socket.socket()
        soc.connect((ServerIp, int(ServerPort)+1))
        upload(soc)
        soc.close()
    elif Command == "Retrieve":
        time.sleep(1)
        soc = socket.socket()
        soc.connect((ServerIp, int(ServerPort) + 1))
        retrieve(soc)
        soc.close()
    elif Command == "Logging":
        log = s.recv(BUF_SIZE)
        print("\n" + log.decode())
    elif Command == "List":
        msg = s.recv(BUF_SIZE)
        print("\n" + msg.decode())
    elif Command == "Quit":
        print("\n Connection closed\n")
        break
s.close()