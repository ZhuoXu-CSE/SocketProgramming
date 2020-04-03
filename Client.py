import socket
import sys

BUF_SIZE = 1024
if len(sys.argv) == 3:
    ServerIp = sys.argv[1]
    ServerPort = sys.argv[2]
else:
    print("\n  Run the program like:\n python3 Client.py < serverip address > <Port number>\n")
    exit(1)
commands = ["Upload", "Retrieve", "Sign in", "Sign out" "Logging", "List"]
s = socket.socket()
s.connect((ServerIp, int(ServerPort)))
print(s.recv(BUF_SIZE).decode())
while True:
    while True:
        Command = input("\nPlease enter command:\n Upload, Retrieve, Sign in, Sign out Logging, List\nCommand:")
        s.send(Command.encode())
        Data = s.recv(BUF_SIZE)
        print(Data.decode())
        if not Data:
            break
    Filename = input("\nPlease enter file name:\n")
    s.send(Filename.encode())
    Filename = "/Users/zx/Desktop/CSE3461Lab/Test/" + Filename
    file = open(Filename, "rb")
    SendData = file.read(BUF_SIZE)
    while SendData:
        s.send(SendData)
        SendData = file.read(BUF_SIZE)
    file.close()
    s.close()
