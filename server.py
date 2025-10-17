import socket
import threading

clients = []
nicknames = []

def broadcast(message, _client):
    for client in clients:
        if client != _client:
            try:
                client.send(message)
            except:
                try:
                    index = clients.index(client)
                    clients.remove(client)
                    client.close()
                    nicknames.pop(index)
                except:
                    pass

def handle_client(conn, addr):
    print(f"[TERHUBUNG] {addr} bergabung ke chat.")
    try:
        # Minta nickname
        conn.send("NICK".encode('utf-8'))
        nickname = conn.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(conn)
        broadcast(f"[INFO] {nickname} bergabung ke chat.".encode('utf-8'), conn)
    except:
        conn.close()
        return

    while True:
        try:
            message = conn.recv(1024)
            if not message:
                break
            broadcast(message, conn)
        except:
            break

    # Saat koneksi berakhir
    try:
        index = clients.index(conn)
        clients.remove(conn)
        conn.close()
        left_nick = nicknames.pop(index)
        broadcast(f"[INFO] {left_nick} keluar dari chat.".encode('utf-8'), None)
        print(f"[PUTUS] {addr} ({left_nick}) keluar dari chat.")
    except:
        pass

def start_server(host='127.0.0.1', port=5555):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"[SERVER BERJALAN] {host}:{port} - Menunggu koneksi...")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == '__main__':
    start_server()
