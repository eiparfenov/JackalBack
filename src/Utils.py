class Vector2i:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def __add__(self, other: 'Vector2i'):
        return Vector2i(self.x + other.x, self.y + other.y)

    def __neg__(self):
        return Vector2i(-self.x, -self.y)

    def __sub__(self, other: 'Vector2i'):
        return Vector2i(self.x - other.x, self.y - other.y)

    def __mul__(self, other: int):
        return Vector2i(self.x * other, self.y * other)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'Vector2i({self.x}, {self.y})'

    def is_in_box(self, box_size):
        return abs(self.x) <= box_size and abs(self.y) <= box_size

    def is_on_side_of_box(self, box_size):
        return (abs(self.x) == box_size + 1 and abs(self.y) <= box_size
                or abs(self.y) == box_size + 1 and abs(self.x) <= box_size)

    def direction_to_center(self):
        if abs(self.x) > abs(self.y):
            if self.x > 0:
                return Vector2i(-1, 0)
            else:
                return Vector2i(1, 0)
        else:
            if self.y > 0:
                return Vector2i(0, -1)
            else:
                return Vector2i(0, -1)

    def rotate(self, rotation: int):
        v = Vector2i(self.x, self.y)
        match rotation:
            case 0:
                pass
            case 1:
                v.x, v.y = v.y, -v.x
            case 2:
                v.x, v.y = -v.x, -v.y
            case 3:
                v.x, v.y = -v.y, v.x,
        return v


class Vector2iUtils:
    DIRECTIONS = (
        Vector2i(x=-1, y=-1),
        Vector2i(x=-1, y=0),
        Vector2i(x=-1, y=1),
        Vector2i(x=0, y=-1),
        Vector2i(x=0, y=1),
        Vector2i(x=1, y=-1),
        Vector2i(x=1, y=0),
        Vector2i(x=1, y=1),
    )
    UP = Vector2i(x=0, y=-1)
    DOWN = Vector2i(x=0, y=1)
    LEFT = Vector2i(x=-1, y=0)
    RIGHT = Vector2i(x=1, y=0)
    DIRECTIONS_STRAIGHT = (
        Vector2i(x=0, y=-1),
        Vector2i(x=0, y=1),
        Vector2i(x=-1, y=0),
        Vector2i(x=1, y=0)
    )
