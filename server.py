import socket
import threading

HOST = "127.0.0.1"
PORT = 12345

clients = []

def handle_client(conn, addr):
    print("Client moi:", addr)
    while True:
        try:
            data = conn.recv(1024)
            if not data or data.decode() == "0":
                break

            message = data.decode()
            print(f"{addr}: {message}")
            response = "Đã nhận: " + message
            conn.send(response.encode())
        except:
            break

    print("Client ngat ket noi:", addr)
    if conn in clients:
        clients.remove(conn)    
    conn.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print("Server dang chay, cho nhieu client ket noi...")

while True:
    conn, addr = server_socket.accept()
    clients.append(conn)

    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
