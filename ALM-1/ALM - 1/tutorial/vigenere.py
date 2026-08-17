def encrypt(text, key):
    key = ''.join(c for c in key.upper() if c.isalpha())
    out, j = [], 0
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            shift = ord(key[j % len(key)]) - ord('A')
            out.append(chr((ord(ch)-base+shift)%26 + base))
            j += 1
        else:
            out.append(ch)
    return ''.join(out)

def decrypt(text, key):
    key = ''.join(c for c in key.upper() if c.isalpha())
    out, j = [], 0
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            shift = ord(key[j % len(key)]) - ord('A')
            out.append(chr((ord(ch)-base-shift)%26 + base))
            j += 1
        else:
            out.append(ch)
    return ''.join(out)

message = input("Enter plaintext: ")
key = input("Enter key: ")
cipher = encrypt(message, key)

print("Plaintext :", message)
print("Ciphertext:", cipher)
print("Decrypted :", decrypt(cipher, key))
