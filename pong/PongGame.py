import json
import threading
import time
from json import JSONDecodeError
from typing import Dict, Any, Optional
from uuid import uuid4

from pong.PongBall import PongBall
from pong.PhysicsObject import PhysicsObject
from pong.PongConfig import PongConfig
from pong.PongPlayer import PongPlayer


class PongGame:
    # Map game IDs to their PongGame instance. Only currently running games should be here.
    # Previous games will be in the database, but not in memory.
    all_games: Dict[str, "PongGame"] = {}

    # Move the ball to the center of the game region
    def center_ball(self):
        center_x = self.config.game_width // 2
        center_y = self.config.game_height // 2
        self.ball.physics_object.x = center_x
        self.ball.physics_object.y = center_y

    # Handle a round victory
    def round_won(self, winner: PongPlayer):
        winner.score += 1
        print(f"{winner.username} won that round. Score: {self.left.score} to {self.right.score}")
        # TODO give ingredient to winner and set up next round
        self.center_ball()

    # Push an element (e.g. a paddle) into the game region if it's not (vertically only)
    def ensure_in_bounds(self, physics_object: PhysicsObject):
        if physics_object.y < 0:
            physics_object.y = 0
        if physics_object.y > self.config.game_height - physics_object.height:
            physics_object.y = self.config.game_height - physics_object.height

    # delta_time is how much time passed since the last frame
    def update_frame(self, delta_time: float):

        # Handle paddle movement
        self.left.paddle.update_position(delta_time)
        self.right.paddle.update_position(delta_time)
        self.ensure_in_bounds(self.right.paddle)
        self.ensure_in_bounds(self.left.paddle)

        # Handle ball movement - TEMPORARY TODO: clean this up
        self.ball.physics_object.update_position(delta_time)
        if self.ball.physics_object.temporary_collides(self.left.paddle) and self.ball.physics_object.x <= self.left.paddle.top_right()[0]:
            # Hit left paddle
            self.ball.physics_object.x = self.left.paddle.x + self.left.paddle.width
            self.ball.physics_object.x_velocity *= -1
        elif self.ball.physics_object.temporary_collides(self.right.paddle) and self.ball.physics_object.x + self.ball.physics_object.width >= self.right.paddle.top_left()[0]:
            # Hit right paddle
            self.ball.physics_object.x = self.right.paddle.x - self.ball.physics_object.width
            self.ball.physics_object.x_velocity *= -1

        # Handle scoring
        # Goal on left (by right)
        if self.ball.physics_object.x + self.ball.physics_object.width < 0:
            self.round_won(self.right)
        # Goal on right (by left)
        elif self.ball.physics_object.x > self.config.game_width:
            self.round_won(self.left)

        # print(f"{delta_time=}")
        # print(f"{time.time()} {self.left.paddle.y=}")
        # TODO put all logic to prepare the next frame here

    def game_loop(self):
        time_per_frame: float = 1 / self.config.framerate
        last_update_time: float = time.time()
        while True:
            frame_start_time: float = time.time()
            time_since_last_frame: float = frame_start_time - last_update_time

            self.update_frame(time_since_last_frame)
            after_update_time: float = time.time()
            time_took_to_update_frame: float = after_update_time - frame_start_time
            time_until_next_frame: float = time_per_frame - time_took_to_update_frame

            # Wait until the next frame should happen to avoid exceeding the target framerate
            if time_until_next_frame > 0:
                # If this frame was rendered faster than the framerate, wait until next frame
                time.sleep(time_until_next_frame)
            # Otherwise, we're lagging behind, so just render the next frame ASAP
            last_update_time = frame_start_time

    def __init__(self, config: PongConfig):
        self.config: PongConfig = config
        self.uid: str = uuid4().hex

        # Create the players and their paddles
        paddle_vertical_center = self.config.game_height // 2 - self.config.paddle_height // 2
        right_paddle_x_position = self.config.game_width - self.config.paddle_width

        left_paddle = PhysicsObject(0, paddle_vertical_center, self.config.paddle_width, self.config.paddle_height)
        self.left = PongPlayer(left_paddle)

        right_paddle = PhysicsObject(right_paddle_x_position, paddle_vertical_center, self.config.paddle_width,
                                     self.config.paddle_height)
        self.right = PongPlayer(right_paddle)

        center_x = self.config.game_width // 2
        center_y = self.config.game_height // 2

        self.ball = PongBall(self.config.ball_height, "", (center_x, center_y), self.config.ball_speed)

        # Add this game to current games
        PongGame.all_games[self.uid] = self

        # Game timing logic
        self.game_thread = threading.Thread(target=self.game_loop)
        self.start_game_loop()

    def start_game_loop(self):
        self.game_thread.start()

    def stop_game_loop(self):
        self.game_thread.join()

    # For writing to the database after the game is complete, NOT for sending to the client
    def to_json(self) -> str:
        d = {
            "id": self.uid,
            "left": self.left.username,
            "right": self.right.username,
            "left_score": self.left.score,
            "right_score": self.right.score,
        }
        return json.dumps(d)

    # Dictionary with info to send to all clients (both players and spectators)
    def to_all_clients(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "id": self.uid,
            "left": self.left.to_dict(),
            "right": self.right.to_dict(),
            "ball": self.ball.to_dict(),
            # TODO more
        }
        return d

    # Return the PongPlayer instance for a given username
    def get_player(self, username: str) -> Optional[PongPlayer]:
        if self.left.username == username:
            return self.left
        if self.right.username == username:
            return self.right
        return None

    # This is error handled in on_websocket_message, so it's okay if an action raises an exception
    def handle_player_input(self, player: PongPlayer, data: Dict[str, Any]):
        velocity = int(data["velocity"])
        if velocity < 0:
            player.paddle.y_velocity = -1 * self.config.paddle_speed
        elif velocity > 0:
            player.paddle.y_velocity = self.config.paddle_speed
        else:
            player.paddle.y_velocity = 0

    # This gets called every time a message is received from the websocket for this game
    def on_websocket_message(self, username: str, message: str):
        print(f"{username=}, {message=}")

        # Identify who sent the message
        this_player: PongPlayer = self.get_player(username)
        if not this_player:
            # Only allow players to influence the game
            print(f"Ignoring command sent from non-player: {username}: {message}")
            return

        # Decode the JSON string
        try:
            d = json.loads(message)
        except JSONDecodeError as e:
            print(f"Error decoding JSON from {username}: '{message}': {e}")
            return

        # Handle the input and potential errors
        try:
            self.handle_player_input(this_player, d)
        except Exception as e:
            print(f"Error handling player input from {username}: '{message}': {e}")

    def __repr__(self):
        return f"PongGame {self.uid} ({self.left.username} vs {self.right.username})"

    def __str__(self):
        return self.__repr__()
