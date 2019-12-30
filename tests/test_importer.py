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
        ["123"],
        ["123123"],
        ["123."],
        ["123.0"],
        ["123.000"],
        ["123.123"],
        ["1.123"],
        ["0.123"],
        [".123"],
        ["000.123"]
    ])
    def test_import_number(self, n):

        importer = MImporter()

        number = importer._getNumber(n, MMarker())

        self.assertTrue(isinstance(number, MNumber))
        self.assertEqual(number.value, n)

    @parameterized.expand([
        ["123mm"],
        ["123123cm"],
        ["123.dm"],
        ["123.0m"],
        ["123.000in"],
        ["123.123pt"],
        ["1.123pc"],
        ["0.123 mm"],
        [".123   cm"],
        ["000.123      dm"]
    ])
    def test_import_length(self, n):

        importer = MImporter()

        length = importer._getLength(n, MMarker())

        self.assertTrue(isinstance(length, MLength))

    @parameterized.expand([
        ["2cm", [["2", "cm"]]],
        ["2cm 2cm", [["2", "cm"], ["2", "cm"]]],
        ["2cm 2cm 2cm 2cm", [["2", "cm"], ["2", "cm"], ["2", "cm"], ["2", "cm"]]],
    ])
    def test_import_length_set(self, text, a):

        importer = MImporter()

        ls = importer._getLengthSet(text, MMarker())

        self.assertEqual(len(ls.lengths), len(a))

    @parameterized.expand([
        ["page-size: a4;", "page-size", "a4"],
        ["page-margin: 2cm 2cm 2cm 2cm;", "page-margin", "2cm 2cm 2cm 2cm"],
        ["font-name: 'Open Sans', sans-serif;", "font-name", "'Open Sans', sans-serif"],
        ["font-colour: hsl(350, 60%, 60%);", "font-colour", "hsl(350, 60%, 60%)"],
    ])
    def test_import_property(self, text, name, value):

        importer = MImporter()

        p = importer._getProperty(text, MMarker())

        self.assertEqual(p.name, name)
        self.assertEqual(str(p.value), value)

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

        ls1 = MLengthSet()
        ls1.lengths.append(MLength("12", "pt"))

        self.assertTrue(isinstance(p1.value, MLengthSet))
        self.assertEqual(len(p1.value.lengths), 1)
        self.assertEqual(str(p1.value), str(ls1))

        self.assertEqual(p2.name, "font-colour")
        self.assertEqual(p2.value, "black")

        self.assertEqual(p3.name, "margin")

        ls2 = MLengthSet()
        ls2.lengths.append(MLength("12", "pt"))
        ls2.lengths.append(MLength("16", "pt"))

        self.assertTrue(isinstance(p3.value, MLengthSet))
        self.assertEqual(len(p3.value.lengths), 2)
        self.assertEqual(str(p3.value), str(ls2))

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
