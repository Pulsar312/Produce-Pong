from datetime import datetime
import json
import random
import threading
import time
from json import JSONDecodeError
from typing import Dict, Any, Optional
from uuid import uuid4

from food.Recipe import Recipe
from pong.HistoricGame import HistoricGame
from pong.PongBall import PongBall
from pong.PhysicsObject import PhysicsObject
from pong.PongConfig import PongConfig
from pong.PongPlayer import PongPlayer


class PongGame:
    # Map game IDs to their PongGame instance. Only currently running games should be here.
    # Previous games will be in the database, but not in memory.
    all_games: Dict[str, "PongGame"] = {}

    # End the game, create a historic game record in the database,
    def game_over(self, winner: PongPlayer):
        # TODO (this order mostly matters)
        #  1. determine if the winner gets an achievement,
        #  2. create a "HistoricGame" with metadata (so a new GET request finds the historic game instead of the live game)
        #  3. Delete this game from all_games
        #  3. set "game_ended" to True,
        #  4. wait several frames to ensure the client gets the "game_over" message
        #  (can wait in this thread because the game state is *sent* to players in a different thread),
        #  5. Stop the game thread

        # TODO we also need the dishes each player made

        winner_earned_achievement: bool = False  # TODO get actual value

        meta: Dict[str, Any] = {
            "winner_earned_achievement": winner_earned_achievement,
            "game_end_date_string": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        historic_game = HistoricGame(self, meta)
        del PongGame.all_games[self.uid]
        self.game_ended = True
        time.sleep(1)
        self.stop_game_loop()

    # Move the ball to the center of the game region
    def center_ball(self):
        center_x = self.config.game_width // 2
        center_y = self.config.game_height // 2
        self.ball.physics_object.x = center_x
        self.ball.physics_object.y = center_y

    def reset_ball(self, winner: PongPlayer):
        if winner == self.right:
            self.ball.physics_object.x_velocity = self.config.ball_speed
        else:
            self.ball.physics_object.x_velocity = (-1) * self.config.ball_speed
        self.ball.physics_object.y_velocity = 0
        self.max_y_speed = self.config.max_y_speed

    # Handle a round victory
    def round_won(self, winner: PongPlayer):
        winner.score += 1
        print(f"{winner.username} won that round. Score: {self.left.score} to {self.right.score}")
        # TODO give ingredient to winner and set up next round
        self.center_ball()
        self.reset_ball(winner)

    def determine_side_collision(self, paddle, collision):
        return collision.height > collision.width

    def collision_update(self, paddle: PhysicsObject):
        # get the bounce back y velocity
        y = 0
        added_velocities = paddle.y_velocity + self.ball.physics_object.y_velocity
        if added_velocities < 0:
            y = max((-1 * self.max_y_speed), added_velocities)
        else:
            y = min(self.max_y_speed, added_velocities)

        # add on some randomness
        if y == 0.0:
            y += random.randint((-1 * self.config.speed_variation), self.config.speed_variation)
        else:
            if self.ball.physics_object.y + (self.ball.physics_object.height / 2) > paddle.y + (paddle.height / 2):
                y += random.randint(0, self.config.speed_variation)
            else:
                y += random.randint((-1) * self.config.speed_variation, 0)

        x = self.ball.physics_object.x_velocity * (-1)

        if self.config.increase_ball_speed_each_hit:
            x *= self.config.increase_ball_speed_multiplier
            self.max_y_speed *= self.config.increase_ball_speed_multiplier

        # set up y and x velocities
        self.ball.physics_object.y_velocity = y
        self.ball.physics_object.x_velocity = x

    # Change the velocity of the ball appropriately depending on how it hit the paddle
    def handle_paddle_ball_collision(self, paddle: PhysicsObject, collision: PhysicsObject):
        if not collision:
            return
        ball: PhysicsObject = self.ball.physics_object

        # Determine if this is a collision from the side or the top/bottom.
        # This can't be quite perfect because we don't have inter-frame information.
        if self.determine_side_collision(paddle, collision):
            # Push the ball back in bounds
            if paddle == self.left.paddle:
                ball.x = paddle.top_right()[0]
            elif paddle == self.right.paddle:
                ball.x = paddle.top_left()[0] - ball.width

            self.collision_update(paddle)

        else:
            # If it hits the top/bottom of the paddle, just bounce it vertically, it's about to score
            ball.y_velocity *= -1
            # TODO prevent overlapping with paddle

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

        # Handle ball movement
        self.ball.physics_object.update_position(delta_time)
        # Check for bouncing on top/bottom walls:
        if self.ball.physics_object.top_left()[1] < 0:
            self.ball.physics_object.y = 0
            self.ball.physics_object.y_velocity *= -1
        elif self.ball.physics_object.bottom_left()[1] > self.config.game_height:
            self.ball.physics_object.y = self.config.game_height - self.config.ball_height
            self.ball.physics_object.y_velocity *= -1

        # Check for hitting paddles
        left_paddle_collision = self.ball.physics_object.intersection(self.left.paddle)
        if left_paddle_collision:
            self.handle_paddle_ball_collision(self.left.paddle, left_paddle_collision)
        else:
            right_paddle_collision = self.ball.physics_object.intersection(self.right.paddle)
            if right_paddle_collision:
                self.handle_paddle_ball_collision(self.right.paddle, right_paddle_collision)

        # Handle scoring
        # Goal on left (by right)
        if self.ball.physics_object.x + self.ball.physics_object.width < 0:
            self.round_won(self.right)
        # Goal on right (by left)
        elif self.ball.physics_object.x > self.config.game_width:
            self.round_won(self.left)

        if self.left.score >= 3:
            self.game_over(self.left)

    def game_loop(self):
        time_per_frame: float = 1 / self.config.framerate
        last_update_time: float = time.time()
        while not self.game_ended:
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
        self.game_started = False  # Changes to true once both players are in
        # TODO implement a wait (countdown?) before the ball starts moving
        self.game_ended = False  # Changes to true once somebody has won

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

        self.max_y_speed = self.config.max_y_speed

        # Add this game to current games
        PongGame.all_games[self.uid] = self

        # Game timing logic
        self.game_thread = threading.Thread(target=self.game_loop)
        self.start_game_loop()

    def start_game_loop(self):
        self.game_thread.start()

    def stop_game_loop(self):
        pass  # Actually, we'll just let the main loop return when the game is over to stop the thread.

    # For writing to the database after the game is complete, NOT for sending to the client
    def to_dict(self) -> Dict[str, Any]:
        d = {
            "id": self.uid,
            "left": self.left.to_dict(),
            "right": self.right.to_dict(),
        }
        return d

    # Dictionary with info to send to all clients (both players and spectators)
    def to_all_clients(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "id": self.uid,
            "left": self.left.to_dict(),
            "right": self.right.to_dict(),
            "ball": self.ball.to_dict(),
            "game_started": self.game_started,
            "game_over": self.game_ended,
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
