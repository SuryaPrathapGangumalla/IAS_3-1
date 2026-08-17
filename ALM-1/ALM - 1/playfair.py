def _matrix(key):
    key = ''.join(c for c in key.upper() if c.isalpha()).replace('J', 'I')
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    chars = []
    for c in key + alphabet:
        if c not in chars:
            chars.append(c)
    return [chars[i:i+5] for i in range(0, 25, 5)]

def _prepare(text):
    text = ''.join(c for c in text.upper() if c.isalpha()).replace('J', 'I')
    pairs, i = [], 0
    while i < len(text):
        a = text[i]
        if i + 1 >= len(text):
            pairs.append(a + 'X')
            i += 1
        elif text[i + 1] == a:
            pairs.append(a + 'X')
            i += 1
        else:
            pairs.append(a + text[i + 1])
            i += 2
    return pairs

def _pos(mat, ch):
    for r in range(5):
        for c in range(5):
            if mat[r][c] == ch:
                return r, c

def encrypt(text, key):
    mat = _matrix(key)
    out = []
    for pair in _prepare(text):
        a, b = pair
        ra, ca = _pos(mat, a)
        rb, cb = _pos(mat, b)
        if ra == rb:
            out += [mat[ra][(ca+1)%5], mat[rb][(cb+1)%5]]
        elif ca == cb:
            out += [mat[(ra+1)%5][ca], mat[(rb+1)%5][cb]]
        else:
            out += [mat[ra][cb], mat[rb][ca]]
    return ''.join(out)

def decrypt(text, key):
    mat = _matrix(key)
    text = ''.join(c for c in text.upper() if c.isalpha()).replace('J','I')
    out = []
    for i in range(0, len(text), 2):
        a, b = text[i:i+2]
        ra, ca = _pos(mat, a)
        rb, cb = _pos(mat, b)
        if ra == rb:
            out += [mat[ra][(ca-1)%5], mat[rb][(cb-1)%5]]
        elif ca == cb:
            out += [mat[(ra-1)%5][ca], mat[(rb-1)%5][cb]]
        else:
            out += [mat[ra][cb], mat[rb][ca]]
    return ''.join(out)
