import unittest
from st_cockroachdb_connection import util


class UnitTests(unittest.TestCase):
    def test_extract_conn_kwargs(self):
        params = ("name", "password", "database")
        target = {"driver": "postgresql", "name": "example", "password": "password",
                  "host": "localhost", "port": "8000", "database": "exampledb"}
        expected = {"name": "example",
                    "password": "password", "database": "exampledb"}
        self.assertEqual(util.extract_conn_kwargs(params, target), expected)


if __name__ == "__main__":
    unittest.main()
