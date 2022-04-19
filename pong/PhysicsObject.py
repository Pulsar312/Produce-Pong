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

    # Calculates whether there is a collision between two PhysicsObjects.
    # Returns True if there is a collision, and False if there is no collision.
    def collision(self, other: "PhysicsObject") -> bool:
        return not ((self.x + self.width <= other.x) or (self.y + self.height <= other.y) or (other.x + other.width <= self.x) or (other.y + other.height <= self.y))

    # Calculate the overlap of this physics object and another
    # Return a rectangular physics object representing the overlap region if it exists, otherwise, None
    def intersection(self, other: "PhysicsObject") -> Optional["PhysicsObject"]:
        if self.collision(other):
            x_val = self.x if self.x > other.x else other.x
            y_val = self.y if self.y > other.y else other.y

            width = abs(other.x + other.width - x_val) if self.x + self.width > other.x + other.width else abs(self.x + self.width - x_val)
            height = abs(other.y + other.height - y_val) if self.y + self.height > other.y + other.height else abs(self.y + self.height - y_val)

            return PhysicsObject(x_val, y_val, width, height)
        else:
            return None

    # A temporary implementation to determine if the ball is colliding with a paddle, really use `intersection` in the future.
    # Returns true if the ball hits the paddle so it needs to change direction
    def temporary_collides(self, paddle: "PhysicsObject") -> bool:
        # Vertical position
        return self.collision(paddle)
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
