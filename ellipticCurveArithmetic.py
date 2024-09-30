import math
import os

# todo: By^2 = x^3 + Ax^2 + x          -   Montgomery Curve
# todo: ax^2 + y^2 = 1 + d(x^2)(y^2)   -   Twisted Edwards Curve


class Point:
    def __init__(self, x=float('inf'), y=float('inf')):
        self.__x = x
        self.__y = y

    def __str__(self):
        return 'Point: Zero' if self.isZero() else f'Point: ({self.__x}, {self.__y})'

    def getPointTuple(self):
        return (self.__x, self.__y)

    def getCopy(self):
        return Point(self.__x, self.__y)

    def isZero(self):
        return self.__x > 10**20 or self.__x < -(10**20)

    def negate(self):
        return Point(self.__x, -self.__y)


class MontgomeryCurve:
    def __init__(self, A, B, p, bits):
        # Form: By^2 = x^3 + Ax^2 + x
        self.A = A # Curve25519 - 486662
        self.B = B # Curve25519 - 1
        self.p = p # Curve25519 - (2**255)-19
        self.bits = bits # Curve25519 - 256
        self.basePoint = Point(9, self.uToY(9%(2**255)))

    def generatePublicKey(self, privateKey):
        return self.bscalarMultiple(self.basePoint, privateKey)

    def encodeUCoordinate(self, u):
        return encodeLittleEndian(u%self.p, self.bits)

    def decodeUCoordinate(self, u):
        uBitsList = [b for b in u]

        if self.bits % 8 != 0:
            uBitsList[-1] &= (1 << (self.bits % 8)) - 1
        return decodeLittleEndian(uBitsList, self.bits)

    def addPoints(self, point1, point2):
        x1, y1 = point1.getPointTuple()
        x2, y2 = point2.getPointTuple()

        if x1 == x2 and y1 == y2:
            return self.doublePoint(point1)
        elif x1 == x2:
            return Point()
        elif point1.isZero():
            return point2
        elif point2.isZero():
            return point1

        try:
            z = (y2 - y1) * inverseMod(x2 - x1, self.p) % self.p
        except ZeroDivisionError:
            raise ValueError('Invalid Coordinates.')

        x3 = (self.B * (z**2) - self.A - x1 - x2)%self.p

        return Point(x3, (z * (x1 - x3) - y1)%self.p)

    def doublePoint(self, point):
        x1, y1 = point.getPointTuple()

        if y1 == 0:
            return Point()

        z = (((3 * (x1**2) + 2 * self.A * x1 + 1)%self.p) * inverseMod((2 * self.B * y1)%self.p, self.p))%self.p

        x2 = (self.B * (z**2) - self.A - 2 * x1)%self.p

        return Point(x2, (z * (x1 - x2) - y1)%self.p)

    def scalarMultiple(self, point, scalar):
        scalarDE = decodeLittleEndian(scalar, self.bits)
        r0 = Point()
        r1 = point
        for i in range(self.bits-1, -1, -1):
            if format(scalarDE, f'{self.bits}b')[i] == 0:
                r1 = self.addPoints(r0, r1)
                r0 = self.doublePoint(r0)
            else:
                r0 = self.addPoints(r0, r1)
                r1 = self.doublePoint(r1)

            assert r1.getPointTuple() == self.addPoints(r0, point).getPointTuple()
        return r0

    def bscalarMultiple(self, point, scalar):
        scalarDE = decodeLittleEndian(scalar, self.bits)
        r0 = Point()
        i = 1
        while i <= scalarDE:
            if i&scalarDE:
                r0 = self.addPoints(r0, point)
            point = self.doublePoint(point)
            i <<= 1
        return r0


    def uToY(self, u):
        return ((u - 1) * inverseMod(u+1, self.p))%self.p

def clamp(privateKey):
    m = bytearray(privateKey)
    m[0] &= 248
    m[31] &= 127
    m[31] |= 64
    return bytes(m)

def generatePrivateKey():
    return clamp(os.urandom(32))

def inverseMod(a, p):
    return pow(a, p-2, p)

def encodeLittleEndian(n, bits):
    return bytes([(n >> 8 * i) & 0xff for i in range((bits + 7) // 8)])

def decodeLittleEndian(b, bits):
    return sum([b[i] << 8 * i for i in range((bits+7) // 8)])

if __name__ == '__main__':
    curve = MontgomeryCurve(486662, 1, (2**255)-19, 256)
    sk = generatePrivateKey()
    pk = curve.generatePublicKey(encodeLittleEndian(7, 256))
    print(f'sk: {sk}\npk: {pk}')
