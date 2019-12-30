import unittest
from parameterized import parameterized

from morphe.core import *


class TestExporter(unittest.TestCase):

    @parameterized.expand([
        [MProperty("page-size", "a4"), "page-size: a4;"],
    ])
    def test_export_property(self, p, text):

        exporter = MExporter()

        self.assertEqual(exporter.exportProperty(p), text)


if __name__ == "__main__":
    unittest.main()