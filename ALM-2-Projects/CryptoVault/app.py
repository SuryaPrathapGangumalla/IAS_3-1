from flask import Flask, render_template, request, jsonify, session
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography import x509
from cryptography.x509.oid import NameOID
from datetime import datetime, timedelta, timezone
import hashlib, secrets, sqlite3, os, base64

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-this-development-secret")
DB = "cryptovault.db"
keys = {}

def db():
    conn = sqlite3.connect(DB)
    conn.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, public_key TEXT NOT NULL)")
    return conn

def ensure_key(username):
    if username not in keys:
        private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        keys[username] = private
    return keys[username]

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/api/register")
def register():
    username = (request.json or {}).get("username", "").strip()
    if not username or len(username) > 40:
        return jsonify(error="Enter a username (1–40 characters)."), 400
    private = ensure_key(username)
    public_pem = private.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo).decode()
    with db() as conn:
        conn.execute("INSERT OR REPLACE INTO users(username, public_key) VALUES (?, ?)", (username, public_pem))
    session["username"] = username
    return jsonify(username=username, public_key=public_pem, message="Demo key pair generated. Private keys remain in server memory.")

@app.get("/api/public-key")
def public_key():
    username = session.get("username")
    if not username:
        return jsonify(error="Register first."), 401
    with db() as conn:
        row = conn.execute("SELECT public_key FROM users WHERE username=?", (username,)).fetchone()
    return jsonify(public_key=row[0] if row else "")

@app.post("/api/rsa/encrypt")
def rsa_encrypt():
    data = request.json or {}
    username = session.get("username")
    if not username:
        return jsonify(error="Register first."), 401
    message = data.get("message", "")
    try:
        cipher = ensure_key(username).public_key().encrypt(message.encode(), padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
        return jsonify(ciphertext=base64.b64encode(cipher).decode())
    except Exception as e:
        return jsonify(error="RSA encryption failed. Keep the message short (RSA-OAEP has a size limit)."), 400

@app.post("/api/rsa/decrypt")
def rsa_decrypt():
    data = request.json or {}
    username = session.get("username")
    if not username:
        return jsonify(error="Register first."), 401
    try:
        cipher = base64.b64decode(data.get("ciphertext", ""), validate=True)
        plain = ensure_key(username).decrypt(cipher, padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
        return jsonify(plaintext=plain.decode())
    except Exception:
        return jsonify(error="Unable to decrypt. Check the ciphertext and current session."), 400

@app.post("/api/rsa/sign")
def rsa_sign():
    username = session.get("username")
    if not username: return jsonify(error="Register first."), 401
    msg = (request.json or {}).get("message", "")
    sig = ensure_key(username).sign(msg.encode(), padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
    return jsonify(signature=base64.b64encode(sig).decode())

@app.post("/api/rsa/verify")
def rsa_verify():
    username = session.get("username")
    if not username: return jsonify(error="Register first."), 401
    data = request.json or {}
    try:
        ensure_key(username).public_key().verify(base64.b64decode(data["signature"]), data.get("message","").encode(),
          padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        return jsonify(valid=True, result="Signature is valid.")
    except Exception:
        return jsonify(valid=False, result="Signature is invalid.")

@app.post("/api/dh")
def dh():
    # Small parameters are deliberately used only to visualize the mathematics.
    p, g = 23, 5
    a, b = secrets.randbelow(10) + 2, secrets.randbelow(10) + 2
    A, B = pow(g, a, p), pow(g, b, p)
    return jsonify(p=p, g=g, alice_private=a, bob_private=b, alice_public=A, bob_public=B,
                   alice_secret=pow(B,a,p), bob_secret=pow(A,b,p), note="Toy parameters for learning only; not secure for real key exchange.")

@app.post("/api/hash")
def hash_message():
    message = (request.json or {}).get("message", "")
    return jsonify(sha512=hashlib.sha512(message.encode()).hexdigest())

@app.post("/api/certificate")
def certificate():
    username = session.get("username")
    if not username: return jsonify(error="Register first."), 401
    private = ensure_key(username)
    subject = issuer = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, username)])
    cert = (x509.CertificateBuilder().subject_name(subject).issuer_name(issuer)
            .public_key(private.public_key()).serial_number(x509.random_serial_number())
            .not_valid_before(datetime.now(timezone.utc))
            .not_valid_after(datetime.now(timezone.utc) + timedelta(days=30))
            .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
            .sign(private, hashes.SHA256()))
    pem = cert.public_bytes(serialization.Encoding.PEM).decode()
    return jsonify(certificate=pem, note="Self-signed demonstration certificate; browsers will not trust it automatically.")

if __name__ == "__main__":
    app.run(debug=True)
