from flask import Flask, render_template, request, jsonify
import secrets, hashlib, base64
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

app = Flask(__name__)
TLS_STEPS = [
("Client Hello", "The client proposes supported protocol versions and cipher suites."),
("Server Hello & Certificate", "The server selects parameters and presents a certificate. A real client validates its trust chain and hostname."),
("Key Establishment", "This teaching simulation creates a random pre-master value and demonstrates public-key encryption."),
("Session Key Derivation", "Both sides derive matching demonstration session keys from the shared secret."),
("Finished", "Both sides verify the handshake transcript before application data is sent.")
]
SSH_STEPS = [
("Protocol Version Exchange", "Client and server announce compatible SSH protocol versions."),
("Key Exchange", "The parties use a Diffie–Hellman-style exchange to agree on a shared secret."),
("Server Authentication", "The client checks the server host key against a trusted known-hosts record."),
("User Authentication", "The user proves identity using a password or public-key authentication."),
("Secure Channel Established", "Encrypted and integrity-protected SSH transport is ready.")
]
@app.get("/")
def index(): return render_template("index.html")
@app.post("/api/handshake")
def handshake():
    data=request.json or {}; kind=data.get("kind","tls"); step=max(0,min(int(data.get("step",0)),4))
    steps=TLS_STEPS if kind=="tls" else SSH_STEPS
    # Reproducible high-level state is not retained; this endpoint illustrates sequence and labels.
    return jsonify(kind=kind, step=step+1, total=len(steps), title=steps[step][0], explanation=steps[step][1], complete=step==4)
@app.post("/api/demo-key")
def demo_key():
    # Demonstration only: uses a fresh ephemeral key for one request.
    private=rsa.generate_private_key(public_exponent=65537,key_size=2048)
    secret=secrets.token_bytes(24)
    encrypted=private.public_key().encrypt(secret,padding.OAEP(mgf=padding.MGF1(hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
    recovered=private.decrypt(encrypted,padding.OAEP(mgf=padding.MGF1(hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
    return jsonify(ciphertext=base64.b64encode(encrypted).decode(), secret_fingerprint=hashlib.sha256(secret).hexdigest(),
                   server_fingerprint=hashlib.sha256(recovered).hexdigest(), matches=secret==recovered,
                   note="Ephemeral RSA demonstration only. Modern TLS commonly uses ephemeral (EC)DHE, not RSA key transport.")
@app.post("/api/ipsec")
def ipsec():
    data=request.json or {}; mode=data.get("mode","transport")
    if mode=="tunnel":
        return jsonify(mode=mode, layers=["New outer IP header","ESP header","Encrypted original IP packet + inner header","ESP authentication/integrity data"], explanation="Tunnel mode encapsulates the original IP packet inside a new outer IP packet.")
    return jsonify(mode=mode, layers=["Original IP header","ESP header","Encrypted transport payload","ESP authentication/integrity data"], explanation="Transport mode protects the IP payload while retaining the original IP header.")
if __name__=="__main__": app.run(debug=True)
