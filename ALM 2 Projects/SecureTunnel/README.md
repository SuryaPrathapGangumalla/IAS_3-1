# SecureTunnel — TLS / SSH / IPsec Visualizer

A Flask educational project that walks through conceptual TLS and SSH handshake steps, demonstrates a short-lived RSA encryption/decryption operation, and visualizes IPsec ESP transport versus tunnel mode.

## Run locally
```bash
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000.

## Modules
- Step-by-step TLS handshake concepts
- Step-by-step SSH connection concepts
- Ephemeral RSA encryption demonstration
- IPsec ESP packet-layer comparison

## Accuracy and safety notes
This is a teaching simulator, not a real TLS/SSH stack. Real modern TLS generally negotiates ephemeral (EC)DHE-based secrets and uses carefully specified transcript/key derivation mechanisms. Certificate validation, hostname checks, SSH host-key trust, and network I/O are described rather than implemented. Do not use this project to secure real traffic.
