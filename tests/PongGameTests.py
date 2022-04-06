import unittest

from pong.PongConfig import PongConfig
from pong.PongGame import PongGame


class Test(unittest.TestCase):

    def test_pong_game_loop(self):
        config = PongConfig(800, 500, 100, 25, 1, 30, 10)
        game = PongGame(config)




if __name__ == '__main__':
    unittest.main()
