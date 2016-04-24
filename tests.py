import unittest

import numpy as np

from mathtools import grad

def assertArrayEq(tc, a, b):
    tc.assertEqual(a.shape, b.shape)
    tc.assertTrue(np.allclose(a,b))

class GradientTest(unittest.TestCase):
    def test_constant_function(self):
        x = np.array([[1,1],[1,1]])
        assertArrayEq(self, np.zeros((2,2,2)), grad(x))
        x = np.array([[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]])
        assertArrayEq(self, np.zeros((5,5,2)), grad(x))
    def test_basic(self):
        v = np.array([[1,2],[1,2]])
        vx = np.array([[[0,1], [0,1]], [[0,1], [0,1]]])
        assertArrayEq(self, vx, grad(v))
    def test_more_complex(self):
        v = np.array([[1,2],[0,3]])
        vx = np.array([[[-1,1], [1,1]], [[-1,3], [1,3]]])
        assertArrayEq(self, vx, grad(v))

unittest.main()