import random
import threading
import time

from pong.PhysicsObject import PhysicsObject
from pong.PongConfig import PongConfig
from pong.PongPlayer import PongPlayer


class PongGame:

    # delta_time is how much time passed since the last frame
    def update_frame(self, delta_time: float):

        self.left.paddle.update_position(delta_time)
        print(f"{delta_time=}")
        print(f"{time.time()} {self.left.paddle.y=}")

        wait: float = random.uniform(0.01, 0.06)
        time.sleep(wait)

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

        # Create the players and their paddles
        paddle_vertical_center = self.config.game_height // 2 - self.config.paddle_height // 2
        right_paddle_x_position = self.config.game_width - self.config.paddle_width

        left_paddle = PhysicsObject(0, paddle_vertical_center, self.config.paddle_width, self.config.paddle_height)
        self.left = PongPlayer(left_paddle)

        right_paddle = PhysicsObject(right_paddle_x_position, paddle_vertical_center, self.config.paddle_width,
                                     self.config.paddle_height)
        self.right = PongPlayer(right_paddle)

        # Game timing logic
        self.game_thread = threading.Thread(target=self.game_loop)

    def start_game_loop(self):
        self.game_thread.start()
