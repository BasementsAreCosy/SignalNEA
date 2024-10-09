from utils import *

class Curve25519:
    def __init__(self):
        self.p = (2**255)-19
        self.a24 = (486662 - 2) // 4
        self.bits = 256

    def decodeUCoordinate(self, u: bytes):
        u_list = [b for b in u]
        # Ignore any unused bits.
        if self.bits % 8:
            u_list[-1] &= (1 << (self.bits % 8)) - 1
        return decodeLittleEndian(u_list, self.bits)

    def encodeUCoordinate(self, u: int):
        u = u % self.p
        return encodeLittleEndian(u, self.bits)

    def scalarMultiplication(self, k: bytes, u: bytes):
        _k = decodeLittleEndian(k, self.bits)
        _u = self.decodeUCoordinate(u)

        x1 = _u
        x2 = 1
        z2 = 0
        x3 = _u
        z3 = 1
        swap = 0

        for t in range(self.bits-1, -1, -1):
            kt = (_k >> t) & 1

            swap ^= kt
            x2, x3 = cswap(swap, x2, x3)
            z2, z3 = cswap(swap, z2, z3)
            swap = kt

            A = (x2 + z2) % self.p
            AA = pow(A, 2, self.p)
            B = (x2 - z2) % self.p
            BB = pow(B, 2, self.p)
            E = (AA - BB) % self.p
            C = (x3 + z3) % self.p
            D = (x3 - z3) % self.p
            DA = (D * A) % self.p
            CB = (C * B) % self.p
            x3 = pow((DA + CB), 2, self.p)
            z3 = (x1 * pow((DA - CB), 2, self.p)) % self.p
            x2 = (AA * BB) % self.p
            z2 = (E * (AA + self.a24 * E)) % self.p

        x2, x3 = cswap(swap, x2, x3)
        z2, z3 = cswap(swap, z2, z3)
        return self.encodeUCoordinate((x2 * pow(z2, self.p-2, self.p)) % self.p)

if __name__ == '__main__':
    curve = Curve25519()

    basePoint = curve.encodeUCoordinate(9)

    As = 7
    Ap = curve.scalarMultiplication(encodeLittleEndian(As, 256), basePoint)

    Bs = 5
    Bp = curve.scalarMultiplication(encodeLittleEndian(Bs, 256), basePoint)

    ASs = curve.decodeUCoordinate(curve.scalarMultiplication(encodeLittleEndian(As, 256), Bp))
    BSs = curve.decodeUCoordinate(curve.scalarMultiplication(encodeLittleEndian(Bs, 256), Ap))

    print(ASs)
    print(BSs)

    print(hex(ASs))
