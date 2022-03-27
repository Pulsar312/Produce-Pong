from typing import Tuple, Optional


class PhysicsObject:
    def __init__(self, x: float, y: float, width: float, height: float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    # Return the absolute coordinates of the top left of this object (x, y)
    def top_left(self) -> Tuple[float, float]:
        return self.x, self.y

    def top_right(self) -> Tuple[float, float]:
        return self.x + self.width, self.y

    def bottom_left(self) -> Tuple[float, float]:
        return self.x, self.y + self.height

    def bottom_right(self) -> Tuple[float, float]:
        return self.x + self.width, self.y + self.height

    def center(self) -> Tuple[float, float]:
        return self.x + self.width / 2, self.y + self.height / 2

    # Calculate the center of the collision location between this and another PhysicsObject
    def intersection(self, other: "PhysicsObject") -> Optional[Tuple[float, float]]:
        pass
