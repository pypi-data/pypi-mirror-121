from typing import Union, Iterable
from unittest import TestCase
from click.testing import CliRunner
from dnastack import __main__ as dnastack_cli
import os


# ASSERTS
def assert_has_property(self: TestCase, obj: dict, attribute: str):
    self.assertTrue(
        attribute in obj,
        msg="obj lacking an attribute. obj: %s, intendedAttribute: %s"
        % (obj, attribute),
    )


# CONFIG
def clear_config():
    os.system("truncate -s 0 ~/.dnastack/config.yaml")


def get_cli_config(runner: CliRunner, key: str):
    result = runner.invoke(
        dnastack_cli.dnastack,
        ["config", "get", key],
    )
    return result.output


def set_cli_config(runner: CliRunner, key: str, val: Union[str, list]):
    if type(val) == list:
        set_command = ["config", "set", key] + val
    else:
        set_command = ["config", "set", key, val]

    runner.invoke(dnastack_cli.dnastack, set_command)


def set_auth_params(runner: CliRunner, auth_params: dict):

    # you have to rename the keys for the cli
    auth_params = {
        "wallet-url": auth_params["wallet_uri"],
        "client-redirect-uri": auth_params["redirect_uri"],
        "client-id": auth_params["client_id"],
        "client-secret": auth_params["client_secret"],
    }
    for key in auth_params.keys():
        set_cli_config(runner, key, auth_params[key])


# AUTH
def login_with_refresh_token(runner: CliRunner, refresh_token: str):
    set_cli_config(runner, "oauth_token", ["refresh_token", refresh_token])
    result = runner.invoke(
        dnastack_cli.dnastack,
        ["auth", "refresh"],
    )
    if result.exit_code != 0:
        raise Exception(f"Could not refresh token: {result.output}")
