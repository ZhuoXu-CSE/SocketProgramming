import socket
import sys

PORT = 0
BUF_SIZE = 1024
if len(sys.argv) == 2:
    PORT = sys.argv[1]
    print("\n Server is listening on port :", PORT, "\n")
else:
    print("\n Run the program like:\n python3 Server.py <Port number>\n")
    exit(1)

commands = ["Upload", "Retrieve", "Sign in", "Sign out" "Logging", "List"]
s = socket.socket()
s.bind(('', int(PORT)))
s.listen()
while True:
    conn, addr = s.accept()
    msg = "\n\n|---------------------------------|\n Hi Client[IP address: " + addr[0] + \
          "], \n ֲֳ**Welcome** \n -Server\n|---------------------------------|\n \n\n"
    conn.send(msg.encode())
    # Receive filename from client side
    Filename = conn.recv(1024)
    if Filename:
        filepath = "/Users/zx/Desktop/CSE3461Lab/Receive/" + Filename.decode()
        File = open(filepath, "wb")
        RecvData = conn.recv(1024)
        while RecvData:
            File.write(RecvData)
            RecvData = conn.recv(1024)
    File.close()
    print("\n File has been Transferred successfully \n")
    conn.close()
    print("\n Server closed the connection \n")

    # Come out from the infinite while loop as the file has been copied from client.
    break
s.close()
