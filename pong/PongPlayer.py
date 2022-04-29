from typing import Dict, Any

from food.chef import Chef
from pong.PhysicsObject import PhysicsObject


class PongPlayer:
    def __init__(self, paddle: PhysicsObject):
        self.username = None
        self.paddle: PhysicsObject = paddle  # This player's pong paddle
        self.chef = Chef()  # The chef representing this player
        self.score = 0  # How many round wins does this player have
        self.ready = False  # If they're ready for the game to begin

    def to_dict(self) -> Dict[str, Any]:
        return {
            "username": self.username,
            "score": self.score,
            "paddle": self.paddle.to_dict(),
            "chef": self.chef.to_dict(),
            "ready": self.ready,
        }
