import socket
import sys

BUF_SIZE = 1024
BASE_ADD = "/Users/zx/Desktop/CSE3461Lab/Test/"

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
    file = open(filename, "rb")
    SendData = file.read(BUF_SIZE)
    while SendData:
        soc.send(SendData)
        SendData = file.read(BUF_SIZE)
    file.close()


def retrieve(soc):
    filename = input("\nPlease enter file name you want to retrieve:\n")
    soc.send(filename.encode())
    if filename:
        filepath = BASE_ADD + filename
        file = open(filepath, "wb")
        recvdata = soc.recv(BUF_SIZE)
        msg = recvdata.decode()
        while recvdata and msg != "File not found":
            file.write(recvdata)
            recvdata = soc.recv(BUF_SIZE)
        file.close()
    print("\n File has been Transferred successfully \n")



commands = ["Upload", "Retrieve", "Logging", "List", "Quit"]
s = socket.socket()
s.connect((ServerIp, int(ServerPort)))
print(s.recv(BUF_SIZE).decode())
user = input("Please input Username and password: ")
s.send(user.encode())
info = s.recv(BUF_SIZE)
if info.decode() == "Welcome":
    print(info.decode())
else:
    while info.decode() == "User not found":
        user = input("Please input Username and password: ")
        s.send(user.encode())
        info = s.recv(BUF_SIZE)
datatran = socket.socket()
datatran.connect((ServerIp, int(ServerPort)+1))
while True:
    Command = input("\nPlease enter command:\n Upload, Retrieve, List, Logging Quit\nCommand:")
    s.send(Command.encode())
    while Command:
        if Command in commands:
            break
        Data = s.recv(BUF_SIZE)
        print(Data.decode())
        Command = input("\nPlease enter command:\n Upload, Retrieve, List, Logging Quit\nCommand:")
        s.send(Command.encode())
    if Command == "Upload":
        upload(datatran)
    elif Command == "Retrieve":
        retrieve(datatran)
    elif Command == "Logging":
        log=datatran.recv(BUF_SIZE)
        print(log.decode())
    elif Command == "List":
        msg = datatran.recv(BUF_SIZE)
        print(msg.decode())
    elif Command == "Quit":
        break
s.close()
datatran.close()