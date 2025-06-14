def F(r: str, k: str) -> str:
    return ''.join(chr((ord(c) ^ ord(k[i % len(k)])) % 256) for i, c in enumerate(r))

def feistelRound(l, r, key, rounds=4):
    for i in range(rounds):
        new_l = r
        f_out = F(r, key[i % len(key)]) 
        new_r = ''.join(chr(ord(l[j]) ^ ord(f_out[j])) for j in range(len(l)))
        l, r = new_l, new_r
    return l + r 

def encrypt(plaintext: str, key: str) -> str:
    while len(plaintext) % 8 != 0:
        plaintext += '\0' 
    ciphertext = ''
    for i in range(0, len(plaintext), 8):
        block = plaintext[i:i+8]
        l, r = block[:4], block[4:]
        encrypted = feistelRound(l, r, key)
        ciphertext += encrypted
    return ciphertext

def decrypt(ciphertext: str, key: str) -> str:
    def reverse_rounds(l, r, key, rounds=4):
        for i in reversed(range(rounds)):
            new_r = l
            f_out = F(new_r, key[i % len(key)])
            new_l = ''.join(chr(ord(r[j]) ^ ord(f_out[j])) for j in range(len(r)))
            l, r = new_l, new_r
        return l + r

    plaintext = ''
    for i in range(0, len(ciphertext), 8):
        block = ciphertext[i:i+8]
        l, r = block[:4], block[4:]
        decrypted = reverse_rounds(l, r, key)
        plaintext += decrypted
    return plaintext.rstrip('\0') 

if __name__ == "__main__":
    plaintext = "john.doe@gmail.com"
    key = "mysecretkey"

    print("Original plaintext:", plaintext)

    encrypted = encrypt(plaintext, key)
    print("Encrypted (raw chars):", encrypted)
    print("Encrypted (as bytes):", encrypted.encode('utf-8'))

    decrypted = decrypt(encrypted, key)
    print("Decrypted:", decrypted)

    assert decrypted == plaintext, "Decryption does not match original!"
    print("Encryption-Decryption Test Passed!")
