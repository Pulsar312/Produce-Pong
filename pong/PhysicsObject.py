from typing import Tuple, Optional, Dict, Any


class PhysicsObject:
    def __init__(self, x: float, y: float, width: float, height: float, x_velocity: float = 0.0, y_velocity: float = 0.0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity

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

    # Calculate the overlap of this physics object and another
    # Return a rectangular physics object representing the overlap region if it exists, otherwise, None
    def intersection(self, other: "PhysicsObject") -> Optional["PhysicsObject"]:
        pass

    # A temporary implementation to determine if the ball is colliding with a paddle, really use `intersection` in the future.
    # Returns true if the ball hits the paddle so it needs to change direction
    def temporary_collides(self, paddle: "PhysicsObject") -> bool:
        # Vertical position
        return paddle.top_left()[1] < self.bottom_right()[1] and paddle.bottom_left()[1] > paddle.top_right()[1]
        # Yes, this is icky and won't really be used, but I need something quick for testing

    # Update the location of this PhysicsObject based on its velocity and how much time has passed
    def update_position(self, time_elapsed: float):
        self.x += self.x_velocity * time_elapsed
        self.y += self.y_velocity * time_elapsed

    def to_dict(self) -> Dict[str, Any]:
        return {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "x_velocity": self.x_velocity,
            "y_velocity": self.y_velocity,
        }
