from math import dist

class Circle:

    def __init__(self, centre, radius):
        self.centre = centre
        self.radius = radius

    def __contains__(self, item):
        if dist(item, self.centre) <= self.radius:
            return True
        else:
            return False
