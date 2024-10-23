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

    def addPoints(self):
        pass


class ed25519:
    def __init__(self):
        self.p = (2 ** 255) - 19
        self.d = (-121665 * inverseModP(121666, self.p)) % self.p
        self.q = (2**252) + 27742317777372353535851937790883648493
        self.bits = 256

    def addPoints(self, P: int, Q: int):
        pass
