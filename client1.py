import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = "127.0.0.1"
PORT = 12345

client_socket.connect((HOST, PORT))

while True:
    message = input("Nhập message gửi đến server (0 để thoát): ")
    client_socket.send(message.encode())
    if message == "0":
        break
    response = client_socket.recv(1024).decode()
    print("Phản hồi từ server:", response)

client_socket.close()
