import socket
import sys

if len(sys.argv) == 3:
    ServerIp = sys.argv[1]
    ServerPort = sys.argv[2]
else:
    print("\n  Run the program like:\n python3 Client.py < serverip address > <Port number>\n")
    exit(1)

s = socket.socket()
s.connect((ServerIp, int(ServerPort)))
print(s.recv(1024).decode())
Filename = input("\nPlease enter file name:\n")
s.send(Filename.encode())
Filename = "/Users/zx/Desktop/CSE3461Lab/Test/" + Filename
file = open(Filename, "rb")
SendData = file.read(1024)
while SendData:
    s.send(SendData)
    SendData = file.read(1024)
file.close()
s.close()
