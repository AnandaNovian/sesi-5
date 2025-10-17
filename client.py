import socket
import threading

def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                # server meminta nickname, tangani di thread utama
                continue
            if message:
                print(message)
        except:
            print("Koneksi ke server terputus.")
            client.close()
            break

def start_client(host='127.0.0.1', port=5555):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
    except Exception as e:
        print(f"Gagal terhubung ke server: {e}")
        return

    # Kirim nickname ke server
    nickname = input("Masukkan nickname: ")
    # Tunggu permintaan NICK dari server
    first = client.recv(1024).decode('utf-8')
    if first == 'NICK':
        client.send(nickname.encode('utf-8'))

    thread_receive = threading.Thread(target=receive_messages, args=(client,), daemon=True)
    thread_receive.start()

    print("Ketik pesan lalu tekan Enter untuk mengirim. Ketik '/quit' untuk keluar.")
    while True:
        try:
            message = input("")
            if message.lower() == '/quit':
                client.close()
                break
            full_message = f"{nickname}: {message}"
            client.send(full_message.encode('utf-8'))
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
            client.close()
            break

if __name__ == '__main__':
    start_client()
