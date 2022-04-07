class PongConfig:
    def __init__(self):
        # These are all reasonable defaults, but they can be changed externally
        # This layout makes it very easy to add future game variables
        self.framerate = 60
        self.ball_height = 30
        self.ball_speed = 100
        self.paddle_height = 100
        self.paddle_width = 20
        self.paddle_speed = 100
        self.game_height = 500
        self.game_width = 800
