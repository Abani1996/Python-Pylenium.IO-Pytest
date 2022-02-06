"""
Frontend Pages module
"""
from fixtures.mainteny.app.ui.pages.dashboard_page import DashboardPage
from fixtures.mainteny.app.ui.pages.login_page import LoginPage
from pylenium.driver import Pylenium

import os


class FrontendPages:
    """
    Used to initialize the `pylenium` driver along with POM classes.
    """

    def __init__(self, py_config):
        os.environ["WDM_LOCAL"] = "1"
        self.py = Pylenium(py_config)

        self.dashboard_page = DashboardPage(self.py)
        self.login_page = LoginPage(self.py)
