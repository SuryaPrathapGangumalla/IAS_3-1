# Cryptography ALM-1

## Objective

Develop Python client-server programs demonstrating classical cryptographic algorithms and S-DES, including message encryption/decryption and S-DES file transfer.

## ALM-1 Requirements

### 1. Client-Server Program

The client lists the following algorithms:

1. Caesar Cipher
2. Playfair Cipher
3. Simple Data Encryption Standard (S-DES)

The client:
- selects an algorithm;
- enters a plaintext message;
- encrypts the message;
- displays the ciphertext;
- sends the ciphertext to the server.

The server:
- receives the ciphertext;
- displays the ciphertext;
- decrypts and displays the plaintext;
- sends an encrypted message back to the client.

The client displays both the returned ciphertext and plaintext.

### 2. Tutorial Problems

Two algorithms have been selected:

- Caesar Cipher
- Vigenère Cipher

### 3. S-DES File Transfer

The S-DES portion also includes:

#### Client → Server
A 1 MB file is encrypted using S-DES, sent to the server, decrypted, and displayed using plaintext/ciphertext previews and file sizes.

#### Server → Client
A 10 KB file is encrypted using S-DES, sent to the client, decrypted, and displayed using plaintext/ciphertext previews and file sizes.

## Folder Structure

```text
Cryptography-ALM-1/
│
├── ALM-1/
│   ├── client.py
│   ├── server.py
│   ├── caesar.py
│   ├── playfair.py
│   ├── sdes.py
│   │
│   ├── tutorial/
│   │   ├── caesar.py
│   │   └── vigenere.py
│   │
│   └── file_transfer/
│       ├── client_to_server.py
│       ├── server_receive.py
│       ├── server_to_client.py
│       ├── client_receive.py
│       ├── client_1MB.txt
│       └── server_10KB.txt
│
└── README.md
```

## How to Run

### Main client-server program

Open two terminals.

Terminal 1:

```bash
cd ALM-1
python server.py
```

Terminal 2:

```bash
cd ALM-1
python client.py
```

### Tutorial algorithms

```bash
cd ALM-1/tutorial
python caesar.py
python vigenere.py
```

### 1 MB Client → Server

Terminal 1:

```bash
cd ALM-1/file_transfer
python server_receive.py
```

Terminal 2:

```bash
cd ALM-1/file_transfer
python client_to_server.py
```

### 10 KB Server → Client

Terminal 1:

```bash
cd ALM-1/file_transfer
python server_to_client.py
```

Terminal 2:

```bash
cd ALM-1/file_transfer
python client_receive.py
```

## Requirements

- Python 3.x
- No third-party packages are required.

## Note

S-DES is an educational simplified version of DES and is not intended for real-world security.
