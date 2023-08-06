import unittest
import pathlib
from ..asgard.exceptions import NoDirectoryFoundError
from ..asgard.utils import get_type, get_dir


class TestAsgard(unittest.TestCase):

    def test_get_type(self):
        self.assertEqual(get_type(pathlib.Path("/home")), "directory")

    def test_get_dir(self):
        self.assertTrue(get_dir(
            "/home/aegir", create_if_missing=False, append_datetime=False,
            suffix=None))

        with self.assertRaises(NoDirectoryFoundError):
            get_dir("/home/asgard", create_if_missing=False,
                    append_datetime=False,        suffix=None)


if __name__ == '__main__':
    unittest.main()
