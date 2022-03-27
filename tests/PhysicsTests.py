import unittest

from pong.PhysicsObject import PhysicsObject


class Test(unittest.TestCase):

    def test_physics_object_edges(self):
        rectangle = PhysicsObject(20, 50, 15, 25)  # At (x = 20, y = 50, width = 15, height = 25)
        self.assertEqual(rectangle.x, 20)
        self.assertEqual(rectangle.y, 50)
        self.assertEqual(rectangle.width, 15)
        self.assertEqual(rectangle.height, 25)
        self.assertEqual(rectangle.top_left(), (20, 50))
        self.assertEqual(rectangle.top_right(), (35, 50))
        self.assertEqual(rectangle.bottom_left(), (20, 75))
        self.assertEqual(rectangle.bottom_right(), (35, 75))
        self.assertEqual(rectangle.center(), (27.5, 62.5))


if __name__ == '__main__':
    unittest.main()
