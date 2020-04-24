# https://docs.python.org/3/library/unittest.html
from unittest import TestCase

from tagging.classifier import feature_dict


class TestFeatureDict(TestCase):

    def test_feature_dict(self):
        sent = 'El gato come pescado .'.split()

        self.maxDiff=None

        fdict = {
            'lower': 'el',
            'istitle': True,
            'isupper': False,
            'isnumeric': False,
            'alower': '',
            'aistitle': False,
            'aisupper': False,
            'aisnumeric': False,
            'plower': 'gato',
            'pistitle': False,
            'pisupper': False,
            'pisnumeric': False,
        }

        self.assertEqual(feature_dict(sent, 0), fdict)
