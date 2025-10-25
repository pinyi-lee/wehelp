import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def slope(self):
        if self.p2.x == self.p1.x:
            return float('inf')
        return (self.p2.y - self.p1.y) / (self.p2.x - self.p1.x)

    def is_parallel(self, other):
        return self.slope() == other.slope()

    def is_perpendicular(self, other):
        m1, m2 = self.slope(), other.slope()
        if m1 == float('inf'):
            return m2 == 0
        if m2 == float('inf'):
            return m1 == 0
        return m1 * m2 == -1

class Circle:
    def __init__(self, center, r):
        self.center = center
        self.r = r

    def area(self):
        return math.pi * self.r ** 2

    def intersects(self, other):
        d = math.dist((self.center.x, self.center.y), (other.center.x, other.center.y))
        return d <= self.r + other.r

class Polygon:
    def __init__(self, points):
        self.points = points

    def perimeter(self):
        s = 0
        for i in range(len(self.points)):
            j = (i + 1) % len(self.points)
            s += math.dist((self.points[i].x, self.points[i].y), (self.points[j].x, self.points[j].y))
        return s

def task1():
    lineA = Line(Point(-6,1),Point(2,4))
    lineB = Line(Point(-6,-1),Point(2,2))
    lineC = Line(Point(-1,6),Point(-4,-4))

    circleA = Circle(Point(6,3),2)
    circleB = Circle(Point(8,1),1)

    polygonA = Polygon([Point(-1,-2),Point(2,0),Point(5,-1),Point(4,-4)])

    print()
    print("Are Line A and Line B parallel?", lineA.is_parallel(lineB))
    print("Are Line C and Line A perpendicular?", lineC.is_perpendicular(lineA))
    print("Print the area of Circle A.:", circleA.area())
    print("Do Circle A and Circle B intersect?", circleA.intersects(circleB))
    print("Print the perimeter of Polygon A.", polygonA.perimeter())
    print()

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Enemy:
    def __init__(self, label, pos, direction):
        self.label = label
        self.pos = pos
        self.direction = direction
        self.hp = 10
        self.alive = True

    def move(self):
        if self.alive:
            self.pos.x += self.direction.x
            self.pos.y += self.direction.y

class Tower:
    def __init__(self, label, pos, attack, attack_range):
        self.label = label
        self.pos = pos
        self.attack = attack
        self.attack_range = attack_range

    def in_range(self, enemy):
        if not enemy.alive:
            return False
        return math.dist((self.pos.x, self.pos.y), (enemy.pos.x, enemy.pos.y)) <= self.attack_range

    def attack_enemies(self, enemies):
        for e in enemies:
            if self.in_range(e):
                e.hp -= self.attack
                if e.hp <= 0:
                    e.alive = False

class BasicTower(Tower):
    def __init__(self, label, pos):
        super().__init__(label, pos, attack=1, attack_range=2)

class AdvancedTower(Tower):
    def __init__(self, label, pos):
        super().__init__(label, pos, attack=2, attack_range=4)

def task2():
    enemies = [
        Enemy("E1", Point(-10, 2), Point(2, -1)),
        Enemy("E2", Point(-8, 0), Point(3, 1)),
        Enemy("E3", Point(-9, -1), Point(3, 0))
    ]

    towers = [
        BasicTower("T1",Point(-3, 2)),
        BasicTower("T2",Point(-1, -2)),
        BasicTower("T3",Point(4, 2)),
        BasicTower("T4",Point(7, 0)),
        AdvancedTower("A1",Point(1, 1)),
        AdvancedTower("A2",Point(4, -3))
    ]

    for _ in range(10):
        for e in enemies:
            e.move()
        for t in towers:
            t.attack_enemies(enemies)

    print()
    for e in enemies:
        print(f"Label: {e.label}, Final Position: ({e.pos.x}, {e.pos.y}), Life Points: {e.hp}")
    print()
    
def main():
    task1()
    task2()

if __name__ == "__main__":
    main()

