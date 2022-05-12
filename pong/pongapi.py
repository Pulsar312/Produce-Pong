# This is the file that we'll use to interact with pong games in an abstract way
import datetime
from typing import Optional, Dict, Any, List

import database
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
# They may actually be in multiple games, so we might want to return more than one. This needs some more thought.
def find_player_current_game(username: str) -> Optional[PongGame]:
    pass  # TODO


def get_current_games() -> List[Dict[str, str]]:
    ret: List[Dict[str, str]] = []
    for game in PongGame.all_games.values():
        if not game.game_ended:
            d = {
                "name": f"{game.left.username} ({game.left.score}) vs {game.right.username} ({game.right.score})",
                "id": game.uid,
            }
            ret.append(d)
    return ret


def get_recent_games() -> List[Dict[str, str]]:
    ret: List[Dict[str, str]] = []
    recent_games = list(database.historic_games.find().sort([("_id", -1)]).limit(25))
    for game in recent_games:
        d = {
            "name": f"{game['game']['left']['username']} ({game['game']['left']['score']}) vs {game['game']['right']['username']} ({game['game']['right']['score']})",
            "id": game["id"],
        }
        ret.append(d)
    return ret


# Remove any games that were created a long time ago that haven't started yet
def clean_up_idle_games():
    number_of_seconds_to_purge: int = 30  # Remove games that have been running for this many seconds without starting
    current_time: datetime = datetime.datetime.now()
    all_games: List[PongGame] = list(PongGame.all_games.values())
    for game in all_games:
        if not game.game_started:
            delta_seconds: int = (current_time - game.game_created_time).seconds
            if delta_seconds > number_of_seconds_to_purge:
                del PongGame.all_games[game.uid]
                game.game_thread_running = False
