import random


class Square(object):
    def description(self):
        raise NotImplementedError()

    def is_movable(self):
        raise NotImplementedError()


class PathSquare(Square):
    def is_movable(self):
        return True


class WallSquare(Square):
    def is_movable(self):
        return False


class CobbleStoneFloor(PathSquare):
    def description(self):
        return """
        This is a cobble stone floor... nothing unusual.
        """


class WetFloor(PathSquare):
    def description(self):
        return """
        This is a wet part of the floor. Be careful, it's slippery.
        """


class StoneWall(WallSquare):
    def description(self):
        return """
        This is a stone wall. You can't pass trough
        """


_WALL_BUILDERS = [
    lambda: StoneWall()
]

_PATH_BUILDERS = [
    lambda: CobbleStoneFloor(),
    lambda: WetFloor()
]


class Map:
    def __init__(self, w, h):
        self.width = w
        self.height = h

        self.squares = []
        for y in range(h):
            for x in range(w):
                if x == 0 or x == (w - 1) or y == 0 or y == (h - 1):
                    self.squares.append(random.choice(_WALL_BUILDERS)())
                else:
                    self.squares.append(random.choice(_PATH_BUILDERS)())

    def get(self, x, y):
        if x < 0 or x >= self.width:
            return None
        if y < 0 or y >= self.height:
            return None
        return self.squares[y * self.width + x]
