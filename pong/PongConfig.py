class PongConfig:
    def __init__(self, game_width: int, game_height: int, paddle_height: int, paddle_width: int,
                 speed_multiplier: float, ball_height: int, framerate: int):
        self.framerate = framerate
        self.ball_height = ball_height
        self.speed_multiplier = speed_multiplier
        self.paddle_height = paddle_height
        self.paddle_width = paddle_width
        self.game_height = game_height
        self.game_width = game_width
