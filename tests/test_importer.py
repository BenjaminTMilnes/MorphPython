import unittest
from parameterized import parameterized

from morph.core import *

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

example2 = """

p.blue.main#big, div.red.main, ul.green {
    font-size: 12pt;
}

"""


class TestImporter(unittest.TestCase):

    @parameterized.expand([
        ["123."],
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
        ["123"],
        ["123abc"],
        ["abcdef"],
        ["ffffff"],
        ["f0f0f0"],
        ["d4d4d4"],
        ["123ABC"],
        ["ABCDEF"],
        ["FFFFFF"],
        ["F0F0F0"],
        ["D4D4D4"],
    ])
    def test_import_hexadecimal_number(self, n):

        importer = MImporter()

        hn = importer._getHexadecimalNumber("#" + n, MMarker())

        self.assertEqual(hn, n)

    @parameterized.expand([
        ["#00000000", 0, 0, 0, 0],
        ["#04050607", 4, 5, 6, 7],
        ["#10101010", 16, 16, 16, 16],
        ["#20304050", 32, 48, 64, 80],
        ["#ffffffff", 255, 255, 255, 255],
        ["#FFFFFFFF", 255, 255, 255, 255],
    ])
    def test_import_hex_rgbacolour(self, t, r, g, b, a):

        importer = MImporter()

        c = importer._getRGBAColour(t, MMarker())

        self.assertEqual(c.r, r)
        self.assertEqual(c.g, g)
        self.assertEqual(c.b, b)
        self.assertEqual(c.a, a)

    @parameterized.expand([
        ["#000000", 0, 0, 0],
        ["#040506", 4, 5, 6],
        ["#101010", 16, 16, 16],
        ["#203040", 32, 48, 64],
        ["#ffffff", 255, 255, 255],
        ["#FFFFFF", 255, 255, 255],
    ])
    def test_import_hex_rgbcolour(self, t, r, g, b):

        importer = MImporter()

        c = importer._getRGBAColour(t, MMarker())

        self.assertEqual(c.r, r)
        self.assertEqual(c.g, g)
        self.assertEqual(c.b, b)
        self.assertEqual(c.a, 0)

    @parameterized.expand([
        ["rgba(0, 0, 0, 0%)", 0, 0, 0, 0],
        ["rgba(100, 0, 0, 0%)", 100, 0, 0, 0],
        ["rgba(100, 120, 200, 0%)", 100, 120, 200, 0],
        ["rgba(100, 120, 200, 50%)", 100, 120, 200, 50],
        ["rgba(255, 255, 255, 100%)", 255, 255, 255, 100],
    ])
    def test_import_rgbacolour(self, t, r, g, b, a):

        importer = MImporter()

        c = importer._getRGBAColour(t, MMarker())

        self.assertEqual(int(c.r.value), r)
        self.assertEqual(int(c.g.value), g)
        self.assertEqual(int(c.b.value), b)
        self.assertEqual(c.a.value, a / 100)

    @parameterized.expand([
        ["rgb(0, 0, 0)", 0, 0, 0],
        ["rgb(100, 0, 0)", 100, 0, 0],
        ["rgb(100, 120, 200)", 100, 120, 200],
        ["rgb(100, 120, 200)", 100, 120, 200],
        ["rgb(255, 255, 255)", 255, 255, 255],
    ])
    def test_import_rgbcolour(self, t, r, g, b):

        importer = MImporter()

        c = importer._getRGBAColour(t, MMarker())

        self.assertEqual(int(c.r.value), r)
        self.assertEqual(int(c.g.value), g)
        self.assertEqual(int(c.b.value), b)

    @parameterized.expand([
        ["hsla(0, 0%, 0%, 0%)", 0, 0, 0, 0],
        ["hsla(60, 100%, 100%, 0%)", 60, 100, 100, 0],
        ["hsla(220, 100%, 100%, 0%)", 220, 100, 100, 0],
        ["hsla(359, 100%, 100%, 0%)", 359, 100, 100, 0],
        ["hsla(120, 50%, 50%, 50%)", 120, 50, 50, 50],
    ])
    def test_import_hslacolour(self, t, h, s, l, a):

        importer = MImporter()

        c = importer._getHSLAColour(t, MMarker())

        self.assertEqual(int(c.h.value), h)
        self.assertEqual(c.s.value, s / 100)
        self.assertEqual(c.l.value, l / 100)
        self.assertEqual(c.a.value, a / 100)

    @parameterized.expand([
        ["black", 0, 0, 0, 0],
        ["red", 255, 0, 0, 0],
        ["blue", 0, 0, 255, 0],
        ["white", 255, 255, 255, 0],
    ])
    def test_import_named_colour(self, t, r, g, b, a):

        importer = MImporter()

        c = importer._getPropertyValue(t, MMarker())
        
        self.assertEqual(c.rgbaColour.r, r)
        self.assertEqual(c.rgbaColour.g, g)
        self.assertEqual(c.rgbaColour.b, b)
        self.assertEqual(c.rgbaColour.a, a)

    @parameterized.expand([
        ["page-size: a4;", "page-size", "a4"],
        ["page-margin: 2cm 2cm 2cm 2cm;", "page-margin", "2cm 2cm 2cm 2cm"],
        ["font-name: 'Open Sans', sans-serif;", "font-name", "'Open Sans', sans-serif"],
        ["font-colour: hsl(350, 60%, 60%);", "font-colour", "hsl(350, 60%, 60%)"],
        ["font-colour: #dd0000;", "font-colour", "#dd0000"],
        ["font-colour: #dd000088;", "font-colour", "#dd000088"],
        ["font-colour: black;", "font-colour", "black"],
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
        self.assertEqual(str(p2.value), "black")

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
        self.assertEqual(str(p4.value), "red")

        self.assertEqual(1, len(sr3.selectors))
        self.assertEqual(1, len(sr3.properties))

        s3 = sr3.selectors[0]

        self.assertEqual(s3.id, "infobox")

    def test_import_example_2(self):

        importer = MImporter()

        d = importer.importDocument(example2)

        self.assertEqual(3, len(d.styleRules))

        sr1 = d.styleRules[0]
        sr2 = d.styleRules[1]
        sr3 = d.styleRules[2]

        self.assertEqual(4, len(sr1.selectors))
        self.assertEqual(3, len(sr2.selectors))
        self.assertEqual(2, len(sr3.selectors))



if __name__ == "__main__":
    unittest.main()
