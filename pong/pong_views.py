# Flask Views for the Pong game
from typing import Optional, Dict, Any

from flask import render_template

from authentication import get_username
from error import simple_error_page
from pong.pongapi import find_historic_game, find_current_game


def handle_game_page_request(request, game_id: str):
    username = get_username(request)
    if not username:
        return simple_error_page("Login Required", "You must be logged in to join a game or view historic game results.", 403)

    historic_game: Optional[Dict[str, Any]] = find_historic_game(game_id)
    if historic_game:
        data = {
            "game": historic_game,
        }
        return render_template("pong_templates/historic_game.html", **data)

    current_game = find_current_game(game_id)
    if current_game:
        # This game does exist, but we might need to assign users
        if not current_game.left.username and not current_game.right.username:
            current_game.left.username = username
        elif not current_game.right.username and current_game.left.username != username:
            current_game.right.username = username
        elif not current_game.left.username and current_game.right.username != username:
            current_game.right.username = username

        data = {
            "game_id": game_id,
            "username": username,
            "game": current_game,
            "game3": current_game.to_all_clients(),
        }
        return render_template("pong_templates/game.html", **data)

    else:
        return simple_error_page("This Game Doesn't Exist!",
                                 "This may be due to one of the following: you didn't copy the full the URL, the game was cancelled due to inactivity, or the server rebooted before the game finished.")
