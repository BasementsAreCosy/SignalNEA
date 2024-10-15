import hashlib

def encodeLittleEndian(n: int, bits: int):
    return bytes([(n >> 8 * i) & 0xff for i in range((bits + 7) // 8)])

def decodeLittleEndian(b: bytes, bits: int):
    return sum([b[i] << 8 * i for i in range((bits + 7) // 8)])

def clampScalar25519(k: bytes):
    k_list = bytearray(k)
    k_list[0] &= 248
    k_list[31] &= 127
    k_list[31] |= 64
    return bytes(k_list)

def cswap(swap: int, x2: int, x3: int) -> tuple[int, int]:
    return (x3, x2) if swap else (x2, x3)

def inverseModP(n: int, p: int):
    return pow(n, p-2, p)

def sha512(x):
    return hashlib.sha512(x).digest()

def sha512ModQ(x, q):
    return int.from_bytes(sha512(x), 'little') % q
