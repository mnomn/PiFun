# How to run:
#   python3 -m unittest 

import sys
sys.path.append('..')

import unittest
from settings import *

class TestSettings(unittest.TestCase):
    json_data = {}

    def setUp(self):
        self.json_data = {Settings.CITY: "jo", Settings.ROTATION: True}

    def test_valid_keys(self):
        settings = Settings(None, self.json_data)
        self.assertTrue(settings.get(Settings.ROTATION))
        self.assertEqual(settings.get(Settings.CITY), "jo")

    def test_invalid_key(self):
        settings = Settings(None, self.json_data)
        self.assertIsNone(settings.get("banan"))

if __name__ == "__main_:":
    unittest.main()

