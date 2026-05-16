# Implement a simple cipher to encrypt text and decrypt text 
'''
    Algorithm Description:
    Trying to recreate S-AES

    Plaintext | Key = 1010 0101 1100 0011 = 0xA5C3
    AddRoundKey RoundKey0
                ExpandKey, Rc = 1001 1001
    SubNibbles
    ShiftRows
    MixColumns
    AddRoundKey RoundKey1
                ExpandKey, Rc = 1100 1100
    SubNibbles
    ShiftRows
    AddRoundKey RoundKey2


    Key Size = 16 bits --> 2 bytes
    Block Size = 16 bits --> 2 bytes
    Rounds = 2 rounds

    | b0 b2 |
    | b1 b3 |
    
    1. AddRoundKey - XOR the 16-bit round key onto the 16-bit state. First column is first byte. Second column is second byte
    | b0 b2 | xor | a0 a2 | = | c0 c2 |
    | b1 b3 |     | a1 a3 |   | c1 c3 |
    2. SubNibbles - Subsitute each byte bi with S(bi)
    | b0 b2 | --> | a0 a2 |
    | b1 b3 |     | a1 a3 |
    3. ShiftRows - 0th row is not shifted, 1st row is shifted left by 1
    | b0 b2 | --> | b0 b2 |
    | b1 b3 |     | b3 a1 |
    4. MixColumns - Matrix Multiplication
    | b0 | = | 1 4 | | a0 |
    | b1 |   | 4 1 | | a1 |
    5. ExpandKey - 
        1) Split 16 bit key into two 8-bit halves: K1, K2
        2) Rotate the nibbles in K2
        3) Take the nibbles and swap them with the SubNibbles
        4) XOR the subsituted output with the round key Rc
        5) XOR the result of step 4 with K1 for K1'
        6) K1' XOR K2 = K2'
        7) K1' + K2' is your new key
'''

s_box_list = [
    0x9, 0x4, 0xA, 0xB, 
    0xD, 0x1, 0x8, 0x5, 
    0x6, 0x2, 0x0, 0x3, 
    0xC, 0xE, 0xF, 0x7
]

def addRoundKey(RK, text):
    return text ^ RK

def subNibbles(text):
    result = 0
    for i in range(4):
        # mask by 0xF and shift by nibble
        shift = i * 4
        temp = (text >> shift) & 0xF
        result = result | (s_box_list[temp] << shift)
    return result   

def shiftRows(text):
    # swap the 0th and 2nd nibble
    nibble1 = (text & 0x0F00) >> 8
    nibble3 = (text & 0xF) << 8
    result = (text & 0xF0F0) | nibble1 | nibble3
    return result

def mul2(nibble):
    shift = (nibble << 1) & 0xF # multiply nibble by 2
    if nibble & 0x8: # if nibble has 1 at bit 3 0x1000, means it will overflow
        return shift ^ 3 # keep first 3 bits
    return shift # otherwise, return normally

def MixColumns(text):
    nibble0 = (text >> 12) & 0xF
    nibble1 = (text >> 8) & 0xF
    nibble2 = (text >> 4) & 0xF
    nibble3 = text & 0xF

    new_nibble0 = nibble0 ^ mul2(mul2(nibble1))
    new_nibble1 = mul2(mul2(nibble0)) ^ nibble1
    new_nibble2 = nibble2 ^ mul2(mul2(nibble3))
    new_nibble3 = mul2(mul2(nibble2)) ^ nibble3

    return new_nibble0 << 12 | new_nibble1 << 8 | new_nibble2 << 4 | new_nibble3
    
def expandKey(Rcon, key):
    K1 = (key >> 8) & 0xFF
    K2 = key & 0xFF

    nibble2 = (key >> 4) & 0xF
    nibble3 = key & 0xF

    subbed_word = (s_box_list[nibble3] << 4) | s_box_list[nibble2]
    new_K1 = (subbed_word ^ Rcon) ^ K1
    new_K2 = new_K1 ^ K2

    return (new_K1 << 8) | new_K2

def encrypt(plaintext, key):
    ciphertext = addRoundKey(key, plaintext)
    
    Rcon = 0x99
    RK1 = expandKey(Rcon, key)

    ciphertext = subNibbles(ciphertext)
    ciphertext = shiftRows(ciphertext)
    ciphertext = MixColumns(ciphertext)
    ciphertext = addRoundKey(RK1, ciphertext)

    Rcon = 0xCC
    RK2 = expandKey(Rcon, RK1)

    ciphertext = subNibbles(ciphertext)
    ciphertext = shiftRows(ciphertext)
    ciphertext = addRoundKey(RK2, ciphertext)

    return ciphertext

'''
    For decryption, we run the rounds in reverse
    AddRoundKey RoundKey2
    ShiftRows
    InverseSubNibbles

    AddRoundKey RoundKey1
    InverseMixColumns
    ShiftRows
    InverseSubNibbles

    AddRoundKey RoundKey0
'''
inv_s_box_list = [
    0xA, 0x5, 0x9, 0xB,
    0x1, 0x7, 0x8, 0xF,
    0x6, 0x0, 0x2, 0x3,
    0xC, 0x4, 0xD, 0xE
]

def InverseSubNibbles(text):
    result = 0
    for i in range(4):
        # mask by 0xF and shift by nibble
        shift = i * 4
        temp = (text >> shift) & 0xF
        result = result | (inv_s_box_list[temp] << shift)
    return result   

def InverseMixColumns(text):
    nibble0 = (text >> 12) & 0xF
    nibble1 = (text >> 8) & 0xF
    nibble2 = (text >> 4) & 0xF
    nibble3 = text & 0xF

    new_nibble0 = (mul2(mul2(mul2(nibble0))) ^ nibble0) ^ mul2(nibble1)
    new_nibble1 = mul2(nibble0) ^ (mul2(mul2(mul2(nibble1))) ^ nibble1)

    new_nibble2 = (mul2(mul2(mul2(nibble2))) ^ nibble2) ^ mul2(nibble3)
    new_nibble3 =  mul2(nibble2) ^ (mul2(mul2(mul2(nibble3))) ^ nibble3)

    return new_nibble0 << 12 | new_nibble1 << 8 | new_nibble2 << 4 | new_nibble3
 
def decrypt(ciphertext, key):
    Rcon = 0x99
    RK1 = expandKey(Rcon, key)

    Rcon = 0xCC
    RK2 = expandKey(Rcon, RK1)

    plaintext = addRoundKey(RK2, ciphertext)
    plaintext = shiftRows(plaintext)
    plaintext = InverseSubNibbles(plaintext)

    plaintext = addRoundKey(RK1, plaintext)
    plaintext = InverseMixColumns(plaintext)
    plaintext = shiftRows(plaintext)
    plaintext = InverseSubNibbles(plaintext)

    plaintext = addRoundKey(key, plaintext)

    return plaintext

def main():
    example_plaintext = 0x3F1B

    master_key = 0xA5C3
    ciphertext = encrypt(example_plaintext, master_key)
    print(f"Encrypted: {hex(ciphertext)}")

    print(f"Decrypted: {hex(decrypt(ciphertext, master_key))}")

if __name__ == "__main__":
    main()