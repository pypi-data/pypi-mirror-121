from asgard.arguments_handler import parse_arguments
from time import sleep
import io
import unittest
from icecream import ic
from .context import asgard
import contextlib
import sys
from distutils.version import LooseVersion

CONFIG_FILE_ARGUMENT = "--config_file=../config/asgard.ajson"
CONFIG_DIR_ARGUMENT = "--config_dir=../config/"
CHECKPOINT_FILE_ARGUMENT = "--checkpoint_file=../checkpoint/test_checkpoint.cjson"
CHECKPOINT_DIR_ARGUMENT = "--checkpoint_dir=../checkpoint/"
VERSION = "1.0.1a"


class test_args(unittest.TestCase):

    def setUp(self):
        self.parser = asgard.arguments_handler.create_parsers(
            "Name", "Description", "Epilog", VERSION)

    def test_parser_no_arguments_error(self):
        f = io.StringIO()
        with contextlib.redirect_stderr(f):
            self.assertRaises(SystemExit,
                              parse_arguments,
                              self.parser, [])
        self.assertIn("usage", f.getvalue())

    def test_parser_no_mode_error(self):
        f = io.StringIO()
        with contextlib.redirect_stderr(f):
            self.assertRaises(SystemExit,
                              parse_arguments,
                              self.parser,
                              [CONFIG_FILE_ARGUMENT])
        self.assertIn("usage", f.getvalue())

    def test_parser_single_mode_no_parameters(self):
        f = io.StringIO()
        with contextlib.redirect_stderr(f):
            self.assertRaises(SystemExit,
                              parse_arguments,
                              self.parser,
                              ["single"])
        self.assertIn("usage", f.getvalue())
        self.assertIn("error", f.getvalue())

    def test_parser_version(self):
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            self.assertRaises(SystemExit,
                              parse_arguments,
                              self.parser,
                              ["-v"])
        self.assertTrue(
            (LooseVersion(VERSION) < LooseVersion(str(f.getvalue()))))

    def test_parser_single_mode_no_checkpoint_no_preview(self):

        parsed_arguments = parse_arguments(self.parser,
                                           ["single",
                                            CONFIG_FILE_ARGUMENT])
        self.assertIn("mode", parsed_arguments)
        self.assertEqual(parsed_arguments.mode, "single")
        self.assertIsNone(parsed_arguments.checkpoint_file)
        self.assertFalse(parsed_arguments.preview)

    def test_parser_single_mode_preview_no_checkpoint(self):
        parsed_arguments = parse_arguments(self.parser,
                                           ["--preview", "single",
                                            CONFIG_FILE_ARGUMENT])
        self.assertIn("mode", parsed_arguments)
        self.assertEqual(parsed_arguments.mode, "single")
        self.assertIsNone(parsed_arguments.checkpoint_file)
        self.assertTrue(parsed_arguments.preview)

    def test_parser_single_mode_checkpoint(self):
        parsed_arguments = parse_arguments(self.parser,
                                           ["--preview", "single",
                                            CONFIG_FILE_ARGUMENT,
                                            CHECKPOINT_FILE_ARGUMENT])
        self.assertIn("mode", parsed_arguments)
        self.assertTrue(parsed_arguments.preview)
        self.assertEqual(parsed_arguments.mode, "single")
        self.assertIn(str(parsed_arguments.checkpoint_file),
                      CHECKPOINT_FILE_ARGUMENT)

    def test_parser_multiple_mode_preview_checkpoint(self):
        parsed_arguments = self.parser.parse_args(
            ["--preview", "multiple",
             CONFIG_DIR_ARGUMENT,
             CHECKPOINT_DIR_ARGUMENT])

        self.assertIn("mode", parsed_arguments)
        self.assertTrue(parsed_arguments.preview)
        self.assertEqual(parsed_arguments.mode, "multiple")
        self.assertIn(str(parsed_arguments.checkpoint_dir),
                      CHECKPOINT_DIR_ARGUMENT)


if __name__ == '__main__':
    sys.exit(unittest.main())
