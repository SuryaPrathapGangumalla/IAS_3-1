# CryptoVault — Public-Key Cryptography Toolkit

CryptoVault is a small Flask learning app demonstrating RSA encryption/decryption, RSA digital signatures, SHA-512 hashing, a toy Diffie–Hellman exchange, and a self-signed X.509 certificate.

## Features
- Demo username and generated RSA key pair
- RSA-OAEP encryption/decryption
- RSA-PSS signature creation and verification
- Diffie–Hellman shared-secret walkthrough
- SHA-512 hashing
- Self-signed certificate output
- SQLite storage for demo public keys

## Run locally
```bash
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000.

## Important limitations
This is an educational prototype, not production PKI. Private keys are held in process memory and disappear on restart; the Diffie–Hellman parameters are intentionally tiny; there is no password authentication, certificate trust chain, rate limiting, or hardened deployment. Never expose Flask's development server to the public internet.
