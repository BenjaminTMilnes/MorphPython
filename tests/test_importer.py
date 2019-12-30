import unittest
from parameterized import parameterized

from morphe.core import *

example1 = """

p {
    font-size: 12pt;
    font-colour   :   black   ;
    margin   :12pt 16pt   ;
}

.red { font-colour: red; }

#infobox {
    border: 1px solid blue;
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

        self.assertEqual(3, len(d.styleRules))

        sr1 = d.styleRules[0]
        sr2 = d.styleRules[1]
        sr3 = d.styleRules[2]

        self.assertEqual(1, len(sr1.selectors))
        self.assertEqual(3, len(sr1.properties))

        p1 = sr1.properties[0]
        p2 = sr1.properties[1]
        p3 = sr1.properties[2]

        self.assertEqual(p1.name, "font-size")
        self.assertEqual(p1.value, "12pt")

        self.assertEqual(p2.name, "font-colour")
        self.assertEqual(p2.value, "black")

        self.assertEqual(p3.name, "margin")
        self.assertEqual(p3.value, "12pt 16pt")

        self.assertEqual(1, len(sr2.selectors))
        self.assertEqual(1, len(sr2.properties))
        
        p4 = sr2.properties[0]

        self.assertEqual(p4.name, "font-colour")
        self.assertEqual(p4.value, "red")

        self.assertEqual(1, len(sr3.selectors))
        self.assertEqual(1, len(sr3.properties))

        s3 = sr3.selectors[0]

        self.assertEqual(s3.id, "infobox")


if __name__ == "__main__":
    unittest.main()
