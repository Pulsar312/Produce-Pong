# This is the file that we'll use to interact with pong games in an abstract way
from typing import Optional, Dict, Any
from database import historic_games
from pong.PongConfig import PongConfig
from pong.PongGame import PongGame


# Create a new pong game in memory, return the PongGame instance
# Both usernames are optional
# If a player isn't specified, the next player to join the game will become that player
def create_new_game(username1: str = "", username2: str = "", config: PongConfig = None) -> PongGame:
    if not config:
        config = PongConfig()  # get a default config
    game = PongGame(config)

    if username1:
        game.left.username = username1
    if username2:
        game.right.username = username2

    return game


# Find a previous game from the database, and return a dictionary with its info, or None if it doesn't exist
def find_historic_game(game_id: str) -> Optional[Dict[str, Any]]:
    result = historic_games.find_one({"id": game_id})
    if result:
        return dict(result)
    return None


# Find a currently running game from memory and return it, or None if the game doesn't exist
def find_current_game(game_id: str) -> Optional[PongGame]:
    if game_id in PongGame.all_games:
        return PongGame.all_games[game_id]
    return None


# Find the game a player is currently in. Useful to prevent playing multiple games simultaneously. Returns None if they're not in a game.
def find_player_current_game(username: str) -> Optional[PongGame]:
    pass  # TODO
