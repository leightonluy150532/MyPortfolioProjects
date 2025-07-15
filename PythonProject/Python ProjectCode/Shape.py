import math

class Shape:
    def __init__(self, *args):
        self.sides = args
    
    def printArea(self):
        # Check number of sides
        if len(self.sides) not in [1, 3, 4]:
            print("Shape Area Error!")
            return
        
        # Circle case (1 argument = diameter)
        if len(self.sides) == 1:
            radius = self.sides[0] / 2
            area = 3.14159 * radius * radius
            print("%.1f" % area)
            return
        
        # Check if all sides are equal for triangle or square
        if not all(side == self.sides[0] for side in self.sides):
            print("Shape Area Error!")
            return
            
        # Equilateral Triangle case (3 equal sides)
        if len(self.sides) == 3:
            side = self.sides[0]
            area = (math.sqrt(3) / 4) * side * side
            print("%.1f" % area)
            return
            
        # Square case (4 equal sides)
        if len(self.sides) == 4:
            side = self.sides[0]
            area = side * side
            print("%.1f" % area)
