from math import *

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

    def addPoints(self, point1, point2):
        x1, y1 = point1.getPointTuple()
        x2, y2 = point2.getPointTuple()

        if x1 == x2 and y1 == y2:
            return self.doublePoint(point1)
        elif x1 == x2:
            'Point at Infinity'

        try:
            z = (y2 - y1) * inverseMod(x2 - x1, self.p) % self.p
        except ZeroDivisionError:
            raise ValueError('Invalid Coordinates.')

        x3 = (self.B * (z**2) - self.A - x1 - x2)%self.p

        return Point(x3, (z * (x1 - x3) - y1)%self.p)

    def doublePoint(self, point):
        x1, y1 = point.getPointTuple()

        if y1 == 0:
            return None # todo: amend, point at infinity, find something better than none

        z = (((3 * (x1**2) + 2 * self.A * x1 + 1)%self.p) * inverseMod((2 * self.B * y1)%self.p, self.p))%self.p

        x2 = (self.B * (z**2) - self.A - 2 * x1)%self.p

        return Point(x2, (z * (x1 - x2) - y1)%self.p)

    def scalarMultiple(self, point, scalar):
        r0 = 0
        r1 = self.p
        for i in range(5, -1, -1):
            pass

def inverseMod(a, p):
    return pow(a, p-2, p)


if __name__ == '__main__':
    curve = MontgomeryCurve(486662, 1, (2**255)-19, 256)
    pointA = Point(0.04, 0.208)
    pointB = Point(1, 4)
    print('a = ' + str(pointA))
    print('b = ' + str(pointB))
    pointC = curve.addPoints(pointA, pointB)
    print('c = ' + str(pointC))
    #pointD = pointC.negate()
    #print('d = ' + str(pointD))
    #print('c + d = ' + str(curve.addPoints(pointC, pointD)))
    #print('a + b + d = ' + str(curve.addPoints(pointA, curve.addPoints(pointB, pointD))))
    #print('a * 12345 = ', str(curve.multiplyPoints(pointA, 12345)))
