from typing import Dict, Any, Optional

from food.Recipe import Recipe
from food.chef import Chef
from pong.PhysicsObject import PhysicsObject


class PongPlayer:
    def __init__(self, paddle: PhysicsObject):
        self.username = None
        self.paddle: PhysicsObject = paddle  # This player's pong paddle
        self.chef = Chef()  # The chef representing this player
        self.score = 0  # How many round wins does this player have
        self.ready = False  # If they're ready for the game to begin
        self.best_recipe: Optional[Recipe] = None
        self.recipe_score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "username": self.username,
            "score": self.score,
            "paddle": self.paddle.to_dict(),
            "chef": self.chef.to_dict(),
            "ready": self.ready,
            "recipe": self.best_recipe.to_dict() if self.best_recipe else None,
            "recipe_score": self.recipe_score,
        }

    def __str__(self):
        return str(self.to_dict())
