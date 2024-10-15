from utils import *

class ed25519:
    def __init__(self):
        self.p = (2 ** 255) - 19
        self.d = (-121665 * inverseModP(121666, self.p)) % self.p
        self.q = (2**252) + 27742317777372353535851937790883648493
        self.bits = 256

    def addPoints(self, P, Q):
        pass # todo: homogenononono point stuff
