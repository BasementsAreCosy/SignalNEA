from utils import *

class HomogenousPoint:
    def __init__(self, X: int, Y: int, Z: int, T: int, p: int):
        self.X = X
        self.Y = Y
        self.Z = Z
        self.T = T
        self.p = p

    def negate(self):
        return HomogenousPoint(-self.X % self.p, self.Y, self.Z, -self.T % self.p)


class ed25519:
    def __init__(self):
        self.p = (2 ** 255) - 19
        self.d = (-121665 * inverseModP(121666, self.p)) % self.p
        self.q = (2**252) + 27742317777372353535851937790883648493
        self.bits = 256

    def addPoints(self, point1, point2):
        A = ((Y1 - X1) * (Y2 - X2)) % p
        B = ((Y1 + X1) * (Y2 + X2)) % p
        C = (T1 * 2 * d * T2) % p
        D = (Z1 * 2 * Z2) % p
        E = (B - A) % p
        F = (D - C) % p
        G = (D + C) % p
        H = (B + A) % p

        X3 = (E * F) % p
        Y3 = (G * H) % p
        T3 = (E * H) % p
        Z3 = (F * G) % p

        return HomogenousPoint(X3, Y3, T3, Z3, self.p)
