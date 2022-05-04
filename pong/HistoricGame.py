from typing import Dict, Any

import database


class HistoricGame:
    def __init__(self, game: "PongGame", meta: Dict[str, Any]):
        # Create a historic game from a game in memory
        d = {
            "id": game.uid,
            "game": game.to_dict(),
            "meta": {
                "winner_earned_achievement": meta.get("winner_earned_achievement", False),
                "game_end_date_string": meta.get("game_end_date_string", "[Missing Date]"),
                "winner": meta.get("winner", "[Missing Winner]"),

            }
        }
        database.historic_games.insert_one(d)
