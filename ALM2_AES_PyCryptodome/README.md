# ALM2 - AES Client-Server File Transfer

## Objective

Implement AES using the **PyCryptodome** package in a client-server application.

### Requirements

1. The client sends a **10 KB human-readable text file** to the server.
   - The client displays plaintext and ciphertext.
   - The server receives, decrypts, and displays plaintext and ciphertext.

2. The server sends a **different 5 KB human-readable text file** to the client.
   - The server displays plaintext and ciphertext.
   - The client receives, decrypts, and displays plaintext and ciphertext.

3. Terminal screenshots are included in the GitHub repository.

## Files

- `client.py` - AES client program.
- `server.py` - AES server program.
- `client_10KB.txt` - exactly 10 KB (10,240 bytes) of human-readable text.
- `server_5KB.txt` - exactly 5 KB (5,120 bytes) of different human-readable text.
- `requirements.txt` - PyCryptodome dependency.
- `screenshots/` - place the terminal screenshots here.

## AES Details

- Library: PyCryptodome
- Algorithm: AES
- Key size: 128 bits (16-byte key)
- Mode: CBC
- Padding: PKCS#7
- Ciphertext is printed as Base64 so binary ciphertext can be displayed safely in the terminal.
- The client generates a random IV for its transmission.
- The server uses an IV for its transmission as well; this classroom implementation keeps the server-to-client IV fixed for reproducibility. In a real application, a fresh random IV should be used for every message.

## Installation

```bash
pip install -r requirements.txt
```

## Execution

Open **two terminals** in this folder.

### Terminal 1 - Server

```bash
python server.py
```

### Terminal 2 - Client

```bash
python client.py
```

Start the server first, then start the client.

## Expected Flow

```text
CLIENT
  |
  |  AES-encrypted 10 KB file
  v
SERVER
  |
  |  AES-encrypted 5 KB file
  v
CLIENT
```

The received files are also written to:

- `client_10KB_received.txt`
- `server_5KB_received.txt`

## Verification

After the programs finish, compare the original and received files.

### Windows PowerShell

```powershell
fc.exe /b client_10KB.txt client_10KB_received.txt
fc.exe /b server_5KB.txt server_5KB_received.txt
```

If the files are identical, the transfer and decryption were successful.

## Screenshots

Save screenshots with names such as:

```text
screenshots/01_server_client_10KB.png
screenshots/02_client_server_5KB.png
screenshots/03_verification.png
```

The screenshots should clearly show:

- Server receiving the 10 KB file and displaying plaintext/ciphertext.
- Client receiving the 5 KB file and displaying plaintext/ciphertext.
- File sizes / successful verification.

## GitHub Upload

```bash
git init
git add .
git commit -m "Implement AES client-server file transfer for ALM2"
git branch -M main
git remote add origin <YOUR_GITHUB_REPOSITORY_URL>
git push -u origin main
```
