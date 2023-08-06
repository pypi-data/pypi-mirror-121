import os
import unittest
from click.testing import CliRunner
import json
from dnastack import __main__ as dnastack_cli
from .. import *


class TestCliConfigCommand(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.data_connect_url = TEST_DATA_CONNECT_URI

    def test_cli_config_add_config_and_list(self):
        result = self.runner.invoke(
            dnastack_cli.dnastack, ["config", "set", "testKey", "testValue"]
        )

        self.assertEqual(result.exit_code, 1)

        self.runner.invoke(
            dnastack_cli.dnastack,
            [
                "config",
                "set",
                "data-connect-url",
                self.data_connect_url,
            ],
        )

        result = self.runner.invoke(dnastack_cli.dnastack, ["config", "list"])

        result_object = json.loads(result.output)

        self.assertEqual(result_object["data-connect-url"], self.data_connect_url)
