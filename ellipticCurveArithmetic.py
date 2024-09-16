class EllipticCurve:
    def __init__(self, a=486662, b=1):
        self.a = a
        self.b = b

    def __str__(self):
        return f'Elliptic curve parameters:\na = {self.a}\nb = {self.b}'

    def addPoints(self, point1, point2):
        if point1.getPoint() == point2.getPoint():
            return self.doublePoint(point1)
        if point1.isZero():
            return point2
        if point2.isZero():
            return point1
        if point2.getPoint()[0] - point1.getPoint()[0] == 0:
            return Point()
        L = (point2.getPoint()[1] - point1.getPoint()[1]) / (point2.getPoint()[0] - point1.getPoint()[0])
        x = (L**2) - point1.getPoint()[0] - point2.getPoint()[0]
        return Point(x, L*(point1.getPoint()[0] - x) - point1.getPoint()[1])

    def multiplyPoints(self, point1, scalar):
        pointCopy = point1.getCopy()
        r = Point()
        i = 1
        while i <= scalar:
            if i & scalar:
                r = self.addPoints(r, pointCopy)
            pointCopy = self.doublePoint(pointCopy)
            i <<= 1
        return r

    def doublePoint(self, point):
        if point.isZero():
            return point
        if point.getPoint()[1] == 0:
            return Point()
        L = 3 * (point.getPoint()[0]**2) / (2 * point.getPoint()[1])
        x = (L**2) - (2 * point.getPoint()[0])
        return Point(x, L * (point.getPoint()[0] - x) - point.getPoint()[1])

    def pointFromY(self, y):
        n = y**2 - self.b
        if n >= 0:
            x = n**(1./3)
        else:
            x = -((-n)**(1./3))
        return Point(x, y)


class Point:
    def __init__(self, x=float('inf'), y=float('inf')):
        self.__x = x
        self.__y = y

    def __str__(self):
        return 'Point: Zero' if self.isZero() else f'Point: ({self.__x}, {self.__y})'

    def getPoint(self):
        return (self.__x, self.__y)

    def getCopy(self):
        return Point(self.__x, self.__y)

    def isZero(self):
        return self.__x > 10**20 or self.__x < -(10**20)

    def negate(self):
        return Point(self.__x, -self.__y)

if __name__ == '__main__':
    curve = EllipticCurve(0, 7)
    pointA = curve.pointFromY(1)
    pointB = curve.pointFromY(2)
    print('a = ' + str(pointA))
    print('b = ' + str(pointB))
    pointC = curve.addPoints(pointA, pointB)
    print('c = ' + str(pointC))
    pointD = pointC.negate()
    print('d = ' + str(pointD))
    print('c + d = ' + str(curve.addPoints(pointC, pointD)))
    print('a + b + d = ' + str(curve.addPoints(pointA, curve.addPoints(pointB, pointD))))
    print('a * 12345 = ', str(curve.multiplyPoints(pointA, 12345)))

