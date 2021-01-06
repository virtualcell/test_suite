import unittest
from report_generation.core import run_sim

class CoreTestCase(unittest.TestCase):
    def test_core(self):
        self.assertEqual(run_sim('ls'), 0)