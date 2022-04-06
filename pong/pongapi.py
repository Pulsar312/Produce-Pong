# This is the file that we'll use to interact with pong games in an abstract way
from typing import Optional


# Create a new pong game, return the PongGame instance
# The first player's username MUST be provided.
# The second player's username is optional.
# If the second player isn't specified, the next player to join the game will become the second player
from pong.PongGame import PongGame


def create_new_game(username1: str, username2: Optional[str] = "") -> PongGame:
    pass


