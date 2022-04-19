import unittest

from pong.PhysicsObject import PhysicsObject


class Test(unittest.TestCase):

    def comparePhysicsObjects(self, obj1: PhysicsObject, obj2: PhysicsObject):
        self.assertEqual(obj1.x, obj2.x)
        self.assertEqual(obj1.y, obj2.y)
        self.assertEqual(obj1.width, obj2.width)
        self.assertEqual(obj1.height, obj2.height)

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

        # object inside of other object: x axis
        obj1 = PhysicsObject(10, 10, 10, 10)
        obj2 = PhysicsObject(11, 15, 5, 10)

        self.assertEqual(obj1.collision(obj2), True)
        self.assertEqual(obj2.collision(obj1), True)

        # object inside of other object: y axis
        obj1 = PhysicsObject(10, 10, 10, 10)
        obj2 = PhysicsObject(15, 12, 10, 5)

        self.assertEqual(obj1.collision(obj2), True)
        self.assertEqual(obj2.collision(obj1), True)

        # object inside of other object: x axis and y axis
        obj1 = PhysicsObject(10, 10, 10, 10)
        obj2 = PhysicsObject(12, 12, 5, 5)

        self.assertEqual(obj1.collision(obj2), True)
        self.assertEqual(obj2.collision(obj1), True)

    def test_intersection(self):
        # Object intersects with itself
        obj1 = PhysicsObject(20, 50, 15, 25)  # At (x = 20, y = 50, width = 15, height = 25)

        computed_obj = obj1.intersection(obj1)
        expected_obj = PhysicsObject(20, 50, 15, 25)
        self.comparePhysicsObjects(computed_obj, expected_obj)

        # Object intersects with object shifted down
        obj1 = PhysicsObject(20, 50, 10, 10)
        obj2 = PhysicsObject(20, 55, 10, 10)

        computed_obj = obj1.intersection(obj2)
        expected_obj = PhysicsObject(20, 55, 10, 5)
        self.comparePhysicsObjects(computed_obj, expected_obj)

        # Object intersects with object shifted up
        obj1 = PhysicsObject(20, 50, 10, 10)
        obj2 = PhysicsObject(20, 45, 10, 10)

        computed_obj = obj1.intersection(obj2)
        expected_obj = PhysicsObject(20, 50, 10, 5)
        self.comparePhysicsObjects(computed_obj, expected_obj)

        # Object intersects with object shifted left
        obj1 = PhysicsObject(20, 50, 10, 10)
        obj2 = PhysicsObject(15, 50, 10, 10)

        computed_obj = obj1.intersection(obj2)
        expected_obj = PhysicsObject(20, 50, 5, 10)
        self.comparePhysicsObjects(computed_obj, expected_obj)

        # Object intersects with object shifted right
        obj1 = PhysicsObject(20, 50, 10, 10)
        obj2 = PhysicsObject(25, 50, 10, 10)

        computed_obj = obj1.intersection(obj2)
        expected_obj = PhysicsObject(25, 50, 5, 10)
        self.comparePhysicsObjects(computed_obj, expected_obj)

        # Object intersects with object shifted down right
        obj1 = PhysicsObject(20, 50, 10, 10)
        obj2 = PhysicsObject(25, 55, 10, 10)

        computed_obj = obj1.intersection(obj2)
        expected_obj = PhysicsObject(25, 55, 5, 5)
        self.comparePhysicsObjects(computed_obj, expected_obj)

        # Object intersects with object shifted up left
        obj1 = PhysicsObject(20, 50, 10, 10)
        obj2 = PhysicsObject(15, 45, 10, 10)

        computed_obj = obj1.intersection(obj2)
        expected_obj = PhysicsObject(20, 50, 5, 5)
        self.comparePhysicsObjects(computed_obj, expected_obj)

        # Object intersects with object shifted down left
        obj1 = PhysicsObject(20, 50, 10, 10)
        obj2 = PhysicsObject(25, 45, 10, 10)

        computed_obj = obj1.intersection(obj2)
        expected_obj = PhysicsObject(25, 50, 5, 5)
        self.comparePhysicsObjects(computed_obj, expected_obj)

        # Object intersects with object shifted up right
        obj1 = PhysicsObject(20, 50, 10, 10)
        obj2 = PhysicsObject(15, 55, 10, 10)

        computed_obj = obj1.intersection(obj2)
        expected_obj = PhysicsObject(20, 55, 5, 5)
        self.comparePhysicsObjects(computed_obj, expected_obj)



if __name__ == '__main__':
    unittest.main()
