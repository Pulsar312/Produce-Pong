from typing import Any, Dict, Tuple

from pong.PhysicsObject import PhysicsObject


class PongBall:
    def __init__(self, height: int, image_url: str, starting_location: Tuple[float, float]):
        self.image_url = image_url
        self.height = height
        self.physics_object = PhysicsObject(starting_location[0] - self.height // 2,
                                            starting_location[1] - self.height // 2,
                                            self.height, self.height)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "height": self.height,
            "image": self.image_url,
            "physics_object": self.physics_object.to_dict(),
        }
