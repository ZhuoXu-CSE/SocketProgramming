import socket
import sys

BUF_SIZE = 1024
if len(sys.argv) == 3:
    ServerIp = sys.argv[1]
    ServerPort = sys.argv[2]
else:
    print("\n  Run the program like:\n python3 Client.py < serverip address > <Port number>\n")
    exit(1)


def upload(soc):
    filename = input("\nPlease enter file name:\n")
    soc.send(filename.encode())
    filename = "/Users/zx/Desktop/CSE3461Lab/Test/" + filename
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
        filepath = "/Users/zx/Desktop/CSE3461Lab/Test/" + filename
        file = open(filepath, "wb")
        recvdata = soc.recv(BUF_SIZE)
        msg = recvdata.decode()
        while recvdata and msg is not "File not found":
            file.write(recvdata)
            recvdata = soc.recv(BUF_SIZE)
        file.close()
    print("\n File has been Transferred successfully \n")


def logging(soc):
    pass


commands = ["Upload", "Retrieve", "Signin", "Logging", "Quit"]
s = socket.socket()
s.connect((ServerIp, int(ServerPort)))
print(s.recv(BUF_SIZE).decode())
datatran = socket.socket()
datatran.connect((ServerIp, int(ServerPort)+1))
while True:
    Command = input("\nPlease enter command:\n Upload, Retrieve, Signin, Logging Quit\nCommand:")
    s.send(Command.encode())
    while Command:
        if Command in commands:
            break
        Data = s.recv(BUF_SIZE)
        print(Data.decode())
        Command = input("\nPlease enter command:\n Upload, Retrieve, Signin, Logging\nCommand:")
        s.send(Command.encode())
    if Command == "Upload":
        upload(datatran)
    elif Command == "Retrieve":
        retrieve(datatran)
    elif Command == "Logging":
        logging(s)
    elif Command == "Quit":
        break
s.close()
datatran.close()