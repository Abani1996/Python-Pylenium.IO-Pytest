"""Module to handle environment variables from environment.json"""

import json
import pytest


class Environment:
    """
    This class loads the environment.json file and stores the necessary data like the url, username, password etc.
    The required key-value from the json file should be defined here, in the __init__() to utilising them
    in the project.
    """

    def __init__(self, mainteny_env):
        """
        :param mainteny_env: is the environment of execution(prod, stg etc).
        """
        self.mainteny_env = mainteny_env
        with open("environment.json", "r", encoding="utf-8") as env_file:
            self.env_globals = json.load(env_file)

    # UI
    @property
    def url(self):
        """environment property"""
        return self.env_globals["app"]["ui"][self.mainteny_env]["url"]

    @property
    def username(self):
        """environment property"""
        return self.env_globals["app"]["ui"][self.mainteny_env]["username"]

    @property
    def password(self):
        """environment property"""
        return self.env_globals["app"]["ui"][self.mainteny_env]["password"]

    # API
    @property
    def api_url(self):
        """environment property"""
        return self.env_globals["app"]["api"][self.mainteny_env]["url"]


@pytest.fixture(scope="session")
def environment(mainteny_env):
    """fixture to easily get environment variables"""
    env_globals = Environment(mainteny_env)
    return env_globals
