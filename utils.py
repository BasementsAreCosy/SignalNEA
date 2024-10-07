def decodeLittleEndian(b, bits):
    return sum([b[i] << 8 * i for i in range((bits + 7) / 8)])

def decodeScalar25519(k):
    k_list = [ord(b) for b in k]
    k_list[0] &= 248
    k_list[31] &= 127
    k_list[31] |= 64
    return decodeLittleEndian(k_list, 255)
