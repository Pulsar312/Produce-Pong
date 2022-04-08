# Flask Views for the Pong game
from flask import render_template

from authentication import get_username
from pong.pongapi import find_historic_game, find_current_game


def handle_game_page_request(request, game_id: str):

    username = get_username(request)
    if not username:
        return "You must be logged in to join a game.", 403

    historic_game = find_historic_game(game_id)
    if historic_game:
        # TODO style better
        return f"This game already ended.\n{historic_game}", 200

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
            "game2": current_game.to_json(),
            "game3": current_game.to_all_clients(),
        }
        return render_template("pong_templates/game.html", **data)

    else:
        return "That game doesn't exist.", 404

