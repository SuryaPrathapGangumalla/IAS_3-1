import socket
import struct
import base64
from pathlib import Path
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

HOST = "127.0.0.1"
PORT = 5000
KEY = b"Sixteen byte key"  # Same AES-128 key as client

def receive_file(sock, output_file):
    iv = recv_exact(sock, AES.block_size)
    length = struct.unpack("!I", recv_exact(sock, 4))[0]
    ciphertext = recv_exact(sock, length)

    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

    Path(output_file).write_bytes(plaintext)

    print("\n========== CLIENT -> SERVER ==========")
    print(f"File       : {output_file}")
    print(f"Plain size : {len(plaintext)} bytes")
    print(f"Cipher size: {len(ciphertext)} bytes")
    print("\n--- CIPHERTEXT (Base64) ---")
    print(base64.b64encode(ciphertext).decode("ascii"))
    print("\n--- PLAINTEXT ---")
    print(plaintext.decode("utf-8"))

def send_file(sock, file_path):
    data = Path(file_path).read_bytes()
    iv = AES.block_size * b"\x00"  # Fixed only for simple classroom demonstration.
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(data, AES.block_size))

    sock.sendall(iv)
    sock.sendall(struct.pack("!I", len(ciphertext)))
    sock.sendall(ciphertext)

    print("\n========== SERVER -> CLIENT ==========")
    print(f"File       : {file_path}")
    print(f"Plain size : {len(data)} bytes")
    print(f"Cipher size: {len(ciphertext)} bytes")
    print("\n--- PLAINTEXT ---")
    print(data.decode("utf-8"))
    print("\n--- CIPHERTEXT (Base64) ---")
    print(base64.b64encode(ciphertext).decode("ascii"))

def recv_exact(sock, n):
    chunks = []
    remaining = n
    while remaining:
        chunk = sock.recv(min(4096, remaining))
        if not chunk:
            raise ConnectionError("Connection closed before all data was received.")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)

    print(f"AES Server listening on {HOST}:{PORT}")
    print("Waiting for client...")

    conn, addr = server.accept()
    with conn:
        print(f"Connected by {addr}")

        receive_file(conn, "client_10KB_received.txt")

        ready = recv_exact(conn, 5)
        if ready != b"READY":
            raise ConnectionError("Unexpected client synchronization message.")

        send_file(conn, "server_5KB.txt")

print("\nAES server completed successfully.")
