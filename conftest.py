"""Used to configure pytest and house the common test fixtures"""
from pylenium.config import PyleniumConfig

import json
import os
import pytest

pytest_plugins = [
    "fixtures.harness.artifacts",
    "fixtures.harness.environment",
    "fixtures.harness.utils",
    "fixtures.mainteny.app.api.mainteny_api",
    "fixtures.mainteny.app.ui.mainteny_ui",
]


def pytest_addoption(parser):
    """Adds ability to get custom pytest command line arguments"""
    parser.addoption(
        "--mainteny_env",
        action="store",
        default=None,
        help="env: what env we are attaching to for testing",
    )
    # pylenium CLI options
    parser.addoption(
        "--browser_choice",
        action="store",
        default="",
        help="The lowercase browser name: chrome | firefox",
    )
    parser.addoption("--remote_url", action="store", default="", help="Grid URL to connect tests to.")
    parser.addoption(
        "--screenshots_on",
        action="store",
        default="",
        help="Should screenshots be saved? true | false",
    )
    parser.addoption(
        "--pylog_level",
        action="store",
        default="",
        help="Set the pylog_level: 'off' | 'info' | 'debug'",
    )
    parser.addoption(
        "--options",
        action="store",
        default="",
        help='Comma-separated list of Browser Options. Ex. "headless, incognito"',
    )
    parser.addoption(
        "--caps",
        action="store",
        default="",
        help='List of key-value pairs. Ex. \'{"name": "value", "boolean": true}\'',
    )
    parser.addoption(
        "--page_load_wait_time",
        action="store",
        default="",
        help="The amount of time to wait for a page load before raising an error. Default is 0.",
    )
    parser.addoption(
        "--extensions",
        action="store",
        default="",
        help='Comma-separated list of extension paths. Ex. "*.crx, *.crx"',
    )
    parser.addoption(
        "--lastname",
        action="store",
        default="",
        help="lastname of person for query",
    )
    parser.addoption(
        "--created_year",
        action="store",
        default="",
        help="calendar year of created date YYYY",
    )
    parser.addoption(
        "--full_name",
        action="store",
        default="",
        help="Full name <First Last>",
    )
    parser.addoption(
        "--num_contact_roles",
        action="store",
        default="",
        help="enter number of minimum contact roles",
    )
    parser.addoption(
        "--split_opportunity_id",
        action="store",
        default="",
        help="enter ID of opportunity to report on",
    )
    parser.addoption(
        "--owner_user_role_name",
        action="store",
        default="",
        help="owner user role name",
    )


@pytest.fixture(scope="session")
def mainteny_env(request):
    """Used to determine which environment variables to use"""
    mainteny_arg = request.config.getoption("--mainteny_env")
    try:
        mainteny_arg = mainteny_arg.lower()
    except AttributeError as e:
        raise AttributeError(f"--mainteny_env is required in order to run this test: {e}") from e

    supported_environments = ["dev", "stg", "prd"]
    if mainteny_arg in supported_environments:
        mainteny_env = mainteny_arg
    else:
        raise Exception(f"{mainteny_arg} is not one of the supported environmentes: {supported_environments}")
    return mainteny_env


@pytest.fixture(scope="session", autouse=True)
def project_root() -> str:
    """The Project (or Workspace) root as a filepath.

    * This conftest.py file should be in the Project Root if not already.
    """
    return os.path.dirname(os.path.abspath(__file__))


@pytest.fixture(scope="session")
def py_config(project_root, request) -> PyleniumConfig:
    """Initialize a PyleniumConfig for each tests

    1. This starts by deserializing the user-created pylenium.json from the Project Root.
    2. If that file is not found, then proceed with Pylenium Defaults.
    3. Then any CLI arguments override their respective key/values.
    """
    try:
        # 1. Load pylenium.json in Project Root, if available
        with open(f"{project_root}/pylenium.json") as file:
            _json = json.load(file)
        config = PyleniumConfig(**_json)
    except FileNotFoundError:
        # 2. pylenium.json not found, proceed with defaults
        config = PyleniumConfig()

    # 3. Override with any CLI args/options
    # Driver Settings
    cli_remote_url = request.config.getoption("--remote_url")
    if cli_remote_url:
        config.driver.remote_url = cli_remote_url

    cli_browser_options = request.config.getoption("--options")
    if cli_browser_options:
        config.driver.options = [option.strip() for option in cli_browser_options.split(",")]

    cli_browser = request.config.getoption("--browser_choice")
    if cli_browser:
        config.driver.browser = cli_browser

    cli_capabilities = request.config.getoption("--caps")
    if cli_capabilities:
        # --caps must be in '{"name": "value", "boolean": true}' format
        # with double quotes around each key. booleans are lowercase.
        config.driver.capabilities = json.loads(cli_capabilities)

    cli_page_wait_time = request.config.getoption("--page_load_wait_time")
    if cli_page_wait_time and cli_page_wait_time.isdigit():
        config.driver.page_load_wait_time = int(cli_page_wait_time)

    # Logging Settings
    cli_pylog_level = request.config.getoption("--pylog_level")
    if cli_pylog_level:
        config.logging.pylog_level = cli_pylog_level

    cli_screenshots_on = request.config.getoption("--screenshots_on")
    if cli_screenshots_on:
        shots_on = True if cli_screenshots_on.lower() == "true" else False
        config.logging.screenshots_on = shots_on

    cli_extensions = request.config.getoption("--extensions")
    if cli_extensions:
        config.driver.extension_paths = [ext.strip() for ext in cli_extensions.split(",")]

    return config
