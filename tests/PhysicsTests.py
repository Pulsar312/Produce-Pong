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

    def test_collisions(self):
        # object overlaps with itself
        # object overlaps with other object
        obj1 = PhysicsObject(20, 50, 15, 25)  # At (x = 20, y = 50, width = 15, height = 25)
        obj2 = PhysicsObject(34.999, 74.8, 15, 25)  # At (x = 34.999, y = 74.8, width = 15, height = 25)

        self.assertEqual(obj1.collision(obj1), True)
        self.assertEqual(obj2.collision(obj2), True)

        self.assertEqual(obj1.collision(obj2), True)
        self.assertEqual(obj2.collision(obj1), True)

        # objects touching, but no collision
        obj1 = PhysicsObject(10, 10, 5, 10) # At (x = 10, y = 10, width = 5, height = 10)
        obj2 = PhysicsObject(15, 20, 2, 2) # At (x = 15, y = 20, width = 2, height = 2)

        self.assertEqual(obj1.collision(obj2), False)
        self.assertEqual(obj2.collision(obj1), False)

        # objects not colliding in either axis
        obj1 = PhysicsObject(10, 10, 5, 10)  # At (x = 10, y = 10, width = 5, height = 10)
        obj2 = PhysicsObject(16, 21, 2, 2)  # At (x = 16, y = 21, width = 2, height = 2)

        self.assertEqual(obj1.collision(obj2), False)
        self.assertEqual(obj2.collision(obj1), False)

        # objects colliding in x axis, but not y axis, so no collision
        obj1 = PhysicsObject(10, 10, 5, 10)  # At (x = 10, y = 10, width = 5, height = 10)
        obj2 = PhysicsObject(14, 20, 2, 2)  # At (x = 14, y = 20, width = 2, height = 2)

        self.assertEqual(obj1.collision(obj2), False)
        self.assertEqual(obj2.collision(obj1), False)

        # objects colliding in y axis, but not x axis, so no collision
        obj1 = PhysicsObject(10, 10, 5, 10)  # At (x = 10, y = 10, width = 5, height = 10)
        obj2 = PhysicsObject(15, 19, 2, 2)  # At (x = 14, y = 20, width = 2, height = 2)

        self.assertEqual(obj1.collision(obj2), False)
        self.assertEqual(obj2.collision(obj1), False)


if __name__ == '__main__':
    unittest.main()
