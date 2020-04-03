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


def upload(connection):
    filename = connection.recv(BUF_SIZE)
    if filename:
        filepath = "/Users/zx/Desktop/CSE3461Lab/Receive/" + Filename.decode()
        file = open(filepath, "wb")
        recvdata = connection.recv(BUF_SIZE)
        while recvdata:
            file.write(recvdata)
            recvdata = connection.recv(BUF_SIZE)
        file.close()
    print("\n File has been Transferred successfully \n")


def retrieve(connection):
    pass


def signin(connection):
    pass


def signout(connection):
    pass


def logging(connection):
    pass


commands = ["Upload", "Retrieve", "Signin", "Signout" "Logging"]
s = socket.socket()
s.bind(('', int(PORT)))
s.listen()
while True:
    conn, addr = s.accept()
    msg = "\nHi Client[IP address: " + addr[0] + "], \n ֲֳ**Welcome** \n -Server\n"
    conn.send(msg.encode())
    Comm = conn.recv(BUF_SIZE)
    while Comm:
        args = Comm.decode().split()
        while args[0] not in commands:
            msg = "Invalid command: " + args[0] + "\n\nCommands:\n  Upload\n  Retrieve\n  Signin\n  Signout\n  Logging" \
                                                  "\n  List\n "
            conn.send(msg.encode())
            Comm = conn.recv(BUF_SIZE)
            args = Comm.decode().split()
        # Receive filename from client side
        if args[0] == "Upload":
            upload(conn)
        elif args[0] == "Retrieve":
            retrieve(conn)
        elif args[0] == "Signin":
            signin(conn)
        elif args[0] == "Signout":
            signout(conn)
        elif args[0] == "Logging":
            logging(conn)
    Comm = conn.recv(BUF_SIZE)
    conn.close()
    print("\n Server closed the connection \n")

    # Come out from the infinite while loop as the file has been copied from client.
    break
s.close()
