import unittest
from parameterized import parameterized

from morphe.core import *


class TestExporter(unittest.TestCase):

    @parameterized.expand([
        [MProperty("page-size", "a4"), "page-size: a4;"],
        [MProperty("   font-colour   ", "   black   "), "font-colour: black;"],
    ])
    def test_export_property(self, p, text):

        exporter = MExporter()

        self.assertEqual(exporter.exportProperty(p), text)

    def test_export_example_1(self):

        d = MDocument()

        sr1 = MStyleRule()
        sr2 = MStyleRule()

        s1 = MElementNameSelector("p")
        s2 = MClassSelector("normal")

        p1 = MProperty("font-name", "'Open Sans'")
        p2 = MProperty("font-colour", "black")
        p3 = MProperty("font-height", "12pt")
        p4 = MProperty("font-colour", "red")

        sr1.selectors = [s1]
        sr1.properties = [p1, p2, p3]

        sr2.selectors = [s2]
        sr2.properties = [p4]

        d.styleRules = [sr1, sr2]

        t = "p {\n\tfont-name: 'Open Sans';\n\tfont-colour: black;\n\tfont-height: 12pt;\n}\n\n.normal {\n\tfont-colour: red;\n}\n\n"

        exporter = MExporter()

        self.assertEqual(exporter.exportDocument(d), t)


if __name__ == "__main__":
    unittest.main()