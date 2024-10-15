import os
from utils import *
from curve25519 import *

montCurve = Curve25519()

def generateSecretKey():
    return clampScalar25519(os.urandom(32))

def generatePublicKey(sk: bytes):
    return montCurve.baseScalarMultiplication(sk)

def generateSharedKey(sk: bytes, pk: bytes):
    return montCurve.scalarMultiplication(sk, pk)

if __name__ == '__main__':
    aliceSK = generateSecretKey()
    bobSK = generateSecretKey()
    alicePK = generatePublicKey(aliceSK)
    bobPK = generatePublicKey(bobSK)

    aliceSS = generateSharedKey(aliceSK, bobPK)
    bobSS = generateSharedKey(bobSK, alicePK)

    print(aliceSS == bobSS)
