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
    pass


def signin(soc):
    pass


def signout(soc):
    pass


def logging(soc):
    pass

commands = ["Upload", "Retrieve", "Sign in", "Sign out" "Logging", "Quit"]
s = socket.socket()
s.connect((ServerIp, int(ServerPort)))
print(s.recv(BUF_SIZE).decode())
while True:
    Command = input("\nPlease enter command:\n Upload, Retrieve, Sign in, Sign out Logging\nCommand:")
    s.send(Command.encode())
    while Command:
        if Command in commands:
            break
        Data = s.recv(BUF_SIZE)
        print(Data.decode())
        Command = input("\nPlease enter command:\n Upload, Retrieve, Sign in, Sign out Logging\nCommand:")
        s.send(Command.encode())
    if Command == "Upload":
        upload(s)
    elif Command == "Retrieve":
        retrieve(s)
    elif Command == "Signin":
        signin(s)
    elif Command == "Signout":
        signout(s)
    elif Command == "Logging":
        logging(s)
    elif Command == "Quit":
        break
s.close()
