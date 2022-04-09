class PongConfig:
    def __init__(self):
        # These are all reasonable defaults, but they can be changed externally
        # This layout makes it very easy to add future game variables
        self.framerate: int = 120
        self.ball_height: int = 30
        self.ball_speed: float = 300.0
        self.paddle_height: int = 100
        self.paddle_width: int = 20
        self.paddle_speed: float = 800.0
        self.game_height: int = 500
        self.game_width: int = 800
        self.increase_ball_speed_each_hit = False
