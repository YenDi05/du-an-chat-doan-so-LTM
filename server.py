import socket
import threading

HOST = "127.0.0.1"
PORT = 12345

clients = []
lock = threading.Lock()

def broadcast(message, sender_conn):
    with lock:
        for client in clients:
            if client != sender_conn:
                try:
                    client.send(message)
                except:
                    clients.remove(client)

def handle_client(conn, addr):
    print("Client moi:", addr)
    conn.send("Chao mung ban den chat room!\n".encode())

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break

            message = f"{addr}: {data.decode()}"
            print(message.strip())

            broadcast(message.encode(), conn)

        except:
            break

    print("Client thoat:", addr)
    with lock:
        if conn in clients:
            clients.remove(conn)
    conn.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print("Server chat dang chay...")

while True:
    conn, addr = server_socket.accept()
    with lock:
        clients.append(conn)

    threading.Thread(
        target=handle_client,
        args=(conn, addr),
        daemon=True
    ).start()
