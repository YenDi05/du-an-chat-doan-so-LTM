import socket
import threading
import random

HOST = "127.0.0.1"
PORT = 12345

clients = []
lock = threading.Lock()

secret_number = random.randint(1, 100)
print(f"DEBUG: So bi mat hien tai la: {secret_number}")

def broadcast(message, exclude=None):
    with lock:
        for client in clients[:]:
            if client == exclude:
                continue
            try:
                client.send(message)
            except:
                clients.remove(client)

def reset_game():
    global secret_number
    secret_number = random.randint(1, 100)
    print(f"---- GAME RESET: So bi mat moi la: {secret_number} ----")

def handle_client(conn, addr):
    conn.send(f"Server: Doan so tu 1 den 100\n".encode())
    broadcast(f"Server: {addr} da tham gia phong chat\n".encode(), exclude=conn)

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break

            msg = data.decode().strip()

            if msg.startswith("/guess"):
                parts = msg.split()
                if len(parts) != 2 or not parts[1].isdigit():
                    conn.send("Server: Cu phap dung la /guess <so>\n".encode())
                else:
                    guess = int(parts[1])

                    broadcast(
                        f"{addr} doan: {guess}\n".encode(),
                        exclude=conn
                    )

                    if guess == secret_number:
                        conn.send("Server: DUNG ROI! Ban da doan DUNG so!\n".encode())
                        broadcast(
                            f"Server: {addr} da doan DUNG so!\n".encode(),
                            exclude=conn
                        )
                        reset_game()
                        broadcast("Server: Bat dau van moi\n".encode())
                    elif guess < secret_number:
                        conn.send("Server: So can tim LON HON\n".encode())
                        broadcast(
                            "Server: So can tim LON HON\n".encode(),
                            exclude=conn
                        )
                    else:
                        conn.send("Server: So can tim NHO HON\n".encode())
                        broadcast(
                            "Server: So can tim NHO HON\n".encode(),
                            exclude=conn
                        )
            else:
                broadcast(f"{addr}: {msg}\n".encode(), exclude=conn)

        except:
            break

    with lock:
        if conn in clients:
            clients.remove(conn)

    broadcast(f"Server: {addr} da roi phong chat\n".encode())
    try:
        conn.close()
    except:
        pass

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print("Server dang chay...")

while True:
    conn, addr = server_socket.accept()
    with lock:
        clients.append(conn)
    threading.Thread(
        target=handle_client,
        args=(conn, addr),
        daemon=True
    ).start()
