#Serveur resau de base :
import socket

host = "127.0.0.1"
port = 5000

monSocket = socket.socket()
monSocket.bind((host, port))

monSocket.listen(1)
conn, addr = monSocket.accept()

print("Connection from: " + str(addr))
while True:
    data = conn.recv(1024).decode()
    if not data:
        break
    print("msg recu : " + data)

    print("on envoie : " + data.upper())
    conn.send(data.upper().encode())

conn.close()
