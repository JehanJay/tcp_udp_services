import socket
import sys

from threading import Thread


def listen_clients(conn):
    global connection
    connection = conn
    while True:
        data1 = conn.recv(4096)
        data = data1.decode()
        print(data)
        if not data:
            print("Empty data packet Received")
            break
    print("[-] Connection removed ")
    conn.close()
    sys.exit()


def tcp_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print("Could not create socket. Error Code: ", str(msg[0]), "Error: ", msg[1])
        sys.exit(0)
    ip = '0.0.0.0'
    port = 1141
    address = (ip, port)
    try:
        s.bind(address)
        print("[-] Socket bound to port " + str(port))
    except socket.error as msg:
        print("Bind failed. Error code: {} Error: {}".format(str(msg[0]), msg[1]))
        sys.exit()
    s.listen(10)
    print("[-] Started listening " + str(ip) + ":" + str(port))

    while True:
        conn, addr = s.accept()
        print("connected")
        t = Thread(target=listen_clients, args=(conn,))
        t.start()

    s.close()


if __name__ == "__main__":
    tcp_service()
