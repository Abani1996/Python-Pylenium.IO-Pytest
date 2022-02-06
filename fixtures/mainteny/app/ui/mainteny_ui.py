"""Fixtures to handle general UI"""
from fixtures.mainteny.app.ui.pages.frontend_pages import FrontendPages

import pytest


def login_steps(frontend, environment):
    """
    Helper function to login to UI
    :param frontend:
    :param environment:
    :return:
    """
    assert "" not in (
        environment.username,
        environment.password,
    ), "Username and password need to be inserted into environment.json"
    frontend.py.visit(environment.url)
    frontend.login_page.login(environment.username, environment.password)
    assert frontend.py.should().contain_url("dashboard"), "URL does not contain 'dashboard'"


@pytest.fixture()
def _user_login(artifacts, frontend, environment):
    """
    Function scoped user login fixture
    :param artifacts:
    :param frontend:
    :param environment:
    :return:
    """
    artifacts.logger.info("Logging in...")
    login_steps(frontend, environment)
    artifacts.logger.info("Successfully logged in with browser.")


@pytest.fixture(scope="function", name="frontend")
def fixture_frontend(py_config):
    """Function scoped frontend fixture"""
    frontend = FrontendPages(py_config)
    yield frontend
    # ToDo: screenshot creation for the failures in function level.
    frontend.py.quit()
