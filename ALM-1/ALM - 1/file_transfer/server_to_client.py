import socket
import struct
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sdes import encrypt_block, decrypt_block

HOST = "127.0.0.1"
PORT = 5001
KEY = "1010000010"

def crypt_file(data, encrypting=True):
    out = bytearray()
    fn = encrypt_block if encrypting else decrypt_block
    for b in data:
        out.append(int(fn(format(b, "08b"), KEY), 2))
    return bytes(out)

def send_packet(sock, data):
    sock.sendall(struct.pack("!Q", len(data)))
    sock.sendall(data)

def recv_exact(sock, n):
    data = bytearray()
    while len(data) < n:
        chunk = sock.recv(min(65536, n-len(data)))
        if not chunk:
            raise ConnectionError("Connection closed.")
        data.extend(chunk)
    return bytes(data)

def recv_packet(sock):
    size = struct.unpack("!Q", recv_exact(sock, 8))[0]
    return recv_exact(sock, size)

# This server sends a 10 KB file to the client.
path = "server_10KB.txt"
data = open(path, "rb").read()
cipher = crypt_file(data, True)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)
    print(f"Server listening on {HOST}:{PORT}")

    conn, addr = server.accept()
    with conn:
        send_packet(conn, cipher)
        print("=== SDES: Server -> Client ===")
        print("Plaintext preview :", data[:64], "...")
        print("Ciphertext preview:", cipher[:64].hex().upper(), "...")
        print("Plaintext bytes   :", len(data))
        print("Ciphertext bytes  :", len(cipher))
        print("10 KB file sent successfully.")
