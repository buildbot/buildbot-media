from unittest import TestCase

from src.module import bumblebee

class BasicTest(TestCase):

    def test_bumblebee(self):
        """
        test sum function
        """

        self.assertEquals(bumblebee(1, 1), 2)