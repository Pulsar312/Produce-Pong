import database
from pong.PongGame import PongGame


class HistoricGame:
    def __init__(self, game: PongGame):
        # Create a historic game from a game in memory
        database.historic_games.insert_one(game.to_dict())
        # TODO more
