from typing import Any, Dict, Tuple

from pong.PhysicsObject import PhysicsObject


class PongBall:
    def __init__(self, height: int, image_url: str, starting_location: Tuple[float, float], velocity: int):
        self.image_url = image_url
        self.physics_object = PhysicsObject(starting_location[0] - height // 2,
                                            starting_location[1] - height // 2,
                                            height, height, velocity, 0)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "image": self.image_url,
            "physics_object": self.physics_object.to_dict(),
        }
