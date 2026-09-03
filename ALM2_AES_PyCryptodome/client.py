import socket
import struct
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

HOST = "127.0.0.1"
PORT = 5000
KEY = b"Sixteen byte key"  # AES-128 key

def send_file(sock, file_path):
    data = Path(file_path).read_bytes()
    iv = get_random_bytes(AES.block_size)

    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(data, AES.block_size))

    # Header: IV (16 bytes) + ciphertext length (4 bytes)
    sock.sendall(iv)
    sock.sendall(struct.pack("!I", len(ciphertext)))
    sock.sendall(ciphertext)

    print("\n========== CLIENT -> SERVER ==========")
    print(f"File       : {file_path}")
    print(f"Plain size : {len(data)} bytes")
    print(f"Cipher size: {len(ciphertext)} bytes")
    print("\n--- PLAINTEXT ---")
    print(data.decode("utf-8"))

    print("\n--- CIPHERTEXT (Base64) ---")
    print(base64.b64encode(ciphertext).decode("ascii"))

def receive_file(sock, output_file):
    iv = recv_exact(sock, AES.block_size)
    length = struct.unpack("!I", recv_exact(sock, 4))[0]
    ciphertext = recv_exact(sock, length)

    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

    Path(output_file).write_bytes(plaintext)

    print("\n========== SERVER -> CLIENT ==========")
    print(f"File       : {output_file}")
    print(f"Plain size : {len(plaintext)} bytes")
    print(f"Cipher size: {len(ciphertext)} bytes")
    print("\n--- CIPHERTEXT (Base64) ---")
    print(base64.b64encode(ciphertext).decode("ascii"))
    print("\n--- PLAINTEXT ---")
    print(plaintext.decode("utf-8"))

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

# pathlib is imported here to keep the main code simple.
from pathlib import Path

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((HOST, PORT))
    print(f"Connected to server at {HOST}:{PORT}")

    send_file(client, "client_10KB.txt")

    # Wait for server to finish receiving before server sends its file.
    client.sendall(b"READY")
    receive_file(client, "server_5KB_received.txt")

print("\nAES client completed successfully.")
