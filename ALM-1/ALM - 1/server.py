import socket
from caesar import encrypt as caesar_encrypt, decrypt as caesar_decrypt
from playfair import encrypt as playfair_encrypt, decrypt as playfair_decrypt
from sdes import encrypt_text as sdes_encrypt, decrypt_text as sdes_decrypt

HOST = "127.0.0.1"
PORT = 5000

def encrypt_message(choice, message, key):
    if choice == "1":
        return caesar_encrypt(message, int(key))
    if choice == "2":
        return playfair_encrypt(message, key)
    if choice == "3":
        return sdes_encrypt(message, key)
    raise ValueError("Invalid algorithm.")

def decrypt_message(choice, cipher, key):
    if choice == "1":
        return caesar_decrypt(cipher, int(key))
    if choice == "2":
        return playfair_decrypt(cipher, key)
    if choice == "3":
        return sdes_decrypt(cipher, key)
    raise ValueError("Invalid algorithm.")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)

    print(f"Server listening on {HOST}:{PORT}")
    conn, addr = server.accept()

    with conn:
        data = conn.recv(65536).decode()
        choice, key, cipher = data.split("|", 2)
        plaintext = decrypt_message(choice, cipher, key)

        print("\n=== Client Message ===")
        print("Client Ciphertext:", cipher)
        print("Client Plaintext :", plaintext)

        reply = input("\nEnter server reply: ")
        reply_cipher = encrypt_message(choice, reply, key)

        print("\n=== Server Message ===")
        print("Server Plaintext :", reply)
        print("Server Ciphertext:", reply_cipher)

        conn.sendall(f"{choice}|{key}|{reply_cipher}".encode())
