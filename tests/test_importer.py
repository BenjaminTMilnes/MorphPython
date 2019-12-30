import unittest
from parameterized import parameterized

from morphe.core import *

example1 = """

p {
    font-size: 12pt;
    font-colour: black;
    margin: 12pt 16pt;
}

.red {
    font-colour: red;
}

"""

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

    def test_import_example_1(self):

        importer = MImporter()

        d = importer.importDocument(example1)

        self.assertEqual(2, len(d.styleRules))

        sr1 = d.styleRules[0]
        sr2 = d.styleRules[1]

        self.assertEqual(3, len(sr1.properties))
        self.assertEqual(1, len(sr2.properties))




if __name__ == "__main__":
    unittest.main()
