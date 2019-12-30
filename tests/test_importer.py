import unittest
from parameterized import parameterized

from morphe.core import *


class TestImporter(unittest.TestCase):

    @parameterized.expand([
        ["page-size: a4;", "page-size", "a4"],
        ["page-margin: 2cm 2cm 2cm 2cm;", "page-margin", "2cm 2cm 2cm 2cm"],
        ["font-name: 'Open Sans', sans-serif;",
            "font-name", "'Open Sans', sans-serif"],
        ["font-colour: hsl(350, 60%, 60%);", "font-colour",
         "hsl(350, 60%, 60%)"],
    ])
    def test_import_property(self, text, name, value):

        importer = MImporter()

        p = importer._getProperty(text, MMarker())

        self.assertEqual(p.name, name)
        self.assertEqual(p.value, value)


if __name__ == "__main__":
    unittest.main()
