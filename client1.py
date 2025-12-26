import socket
import threading

HOST = "127.0.0.1"
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

def receive():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print("\n" + message)
        except:
            break

def send():
    while True:
        msg = input()
        if msg.lower() == "exit":
            client_socket.close()
            break
        client_socket.send(msg.encode())

threading.Thread(target=receive, daemon=True).start()
send()
