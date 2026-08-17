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

print("=== Cryptography Client ===")
print("1. Caesar Cipher")
print("2. Playfair Cipher")
print("3. SDES")
choice = input("Choose algorithm (1/2/3): ").strip()

if choice == "1":
    key = input("Enter Caesar shift (e.g. 3): ").strip()
elif choice == "2":
    key = input("Enter Playfair key: ").strip()
elif choice == "3":
    key = input("Enter 10-bit SDES key: ").strip()
else:
    raise SystemExit("Invalid choice.")

message = input("Enter message: ")
cipher = encrypt_message(choice, message, key)

print("\nClient Plaintext :", message)
print("Client Ciphertext:", cipher)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    payload = f"{choice}|{key}|{cipher}".encode()
    s.sendall(payload)
    response = s.recv(65536).decode()

server_choice, server_key, server_cipher = response.split("|", 2)
server_plain = decrypt_message(server_choice, server_cipher, server_key)

print("\n--- Server Reply ---")
print("Server Ciphertext:", server_cipher)
print("Server Plaintext :", server_plain)
