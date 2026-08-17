# Simplified DES (S-DES) implementation.
P10 = [3,5,2,7,4,10,1,9,8,6]
P8  = [6,3,7,4,8,5,10,9]
P4  = [2,4,3,1]
IP  = [2,6,3,1,4,8,5,7]
IP_INV = [4,1,3,5,7,2,8,6]
EP  = [4,1,2,3,2,3,4,1]
S0 = [[1,0,3,2],[3,2,1,0],[0,2,1,3],[3,1,3,2]]
S1 = [[0,1,2,3],[2,0,1,3],[3,0,1,0],[2,1,0,3]]

def perm(bits, table):
    return ''.join(bits[i-1] for i in table)

def ls(bits, n):
    return bits[n:] + bits[:n]

def keygen(key):
    key = ''.join(c for c in key if c in '01')
    if len(key) != 10:
        raise ValueError("S-DES key must be exactly 10 bits.")
    p = perm(key, P10)
    l, r = p[:5], p[5:]
    l, r = ls(l,1), ls(r,1)
    k1 = perm(l+r, P8)
    l, r = ls(l,2), ls(r,2)
    k2 = perm(l+r, P8)
    return k1, k2

def xor(a,b):
    return ''.join('1' if x != y else '0' for x,y in zip(a,b))

def sbox(bits, box):
    row = int(bits[0]+bits[3], 2)
    col = int(bits[1]+bits[2], 2)
    return format(box[row][col], '02b')

def fk(bits, key):
    l, r = bits[:4], bits[4:]
    ep = perm(r, EP)
    x = xor(ep, key)
    s = sbox(x[:4], S0) + sbox(x[4:], S1)
    p4 = perm(s, P4)
    return xor(l, p4) + r

def encrypt_block(bits, key):
    k1, k2 = keygen(key)
    x = perm(bits, IP)
    x = fk(x, k1)
    x = x[4:] + x[:4]
    x = fk(x, k2)
    return perm(x, IP_INV)

def decrypt_block(bits, key):
    k1, k2 = keygen(key)
    x = perm(bits, IP)
    x = fk(x, k2)
    x = x[4:] + x[:4]
    x = fk(x, k1)
    return perm(x, IP_INV)

def text_to_bits(text):
    return ''.join(format(b, '08b') for b in text.encode('utf-8'))

def bits_to_bytes(bits):
    return bytes(int(bits[i:i+8],2) for i in range(0,len(bits),8))

def encrypt_text(text, key):
    data = text.encode('utf-8')
    out = bytearray()
    for b in data:
        block = format(b, '08b')
        out.append(int(encrypt_block(block, key), 2))
    return bytes(out).hex().upper()

def decrypt_text(cipher_hex, key):
    data = bytes.fromhex(cipher_hex)
    out = bytearray()
    for b in data:
        block = format(b, '08b')
        out.append(int(decrypt_block(block, key), 2))
    return out.decode('utf-8', errors='replace')
