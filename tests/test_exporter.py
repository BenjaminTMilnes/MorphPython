import unittest
from parameterized import parameterized

from morph.core import *


class TestExporter(unittest.TestCase):

    @parameterized.expand([
        [MProperty("page-size", "a4"), "page-size: a4;"],
        [MProperty("   font-colour   ", "   black   "), "font-colour: black;"],
    ])
    def test_export_property(self, p, text):

        self.assertEqual(str(p), text)

    def test_export_example_1(self):

        d = MDocument()

        sr1 = MStyleRule()
        sr2 = MStyleRule()
        sr3 = MStyleRule()

        s1 = MElementNameSelector("p")
        s2 = MClassSelector("normal")
        s3 = MIdSelector("infobox")

        p1 = MProperty("font-name", "'Open Sans'")
        p2 = MProperty("font-colour", "black")
        p3 = MProperty("font-height", "12pt")
        p4 = MProperty("font-colour", "red")
        p5 = MProperty("border", "1px solid blue")

        sr1.selectors = [s1]
        sr1.properties = [p1, p2, p3]

        sr2.selectors = [s2]
        sr2.properties = [p4]

        sr3.selectors = [s3]
        sr3.properties = [p5]

        d.styleRules = [sr1, sr2, sr3]

        t = "p {\n\tfont-name: 'Open Sans';\n\tfont-colour: black;\n\tfont-height: 12pt;\n}\n\n.normal {\n\tfont-colour: red;\n}\n\n#infobox {\n\tborder: 1px solid blue;\n}\n\n"

        exporter = MExporter()

        self.assertEqual(exporter.exportDocument(d), t)


if __name__ == "__main__":
    unittest.main()