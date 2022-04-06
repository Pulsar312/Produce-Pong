from food.chef import Chef
from pong.PhysicsObject import PhysicsObject


class PongPlayer:
    def __init__(self, paddle: PhysicsObject):
        self.paddle = paddle  # This player's pong paddle
        self.chef = Chef()  # The chef representing this player
        self.score = 0  # How many round wins does this player have
