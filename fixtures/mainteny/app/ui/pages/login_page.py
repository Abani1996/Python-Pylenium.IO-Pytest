"""
Login Module
"""
from selenium.webdriver.support import expected_conditions as ec
from fixtures.mainteny.app.ui.pages.page_base import PageBase
from pylenium.element import Element


class LoginPage(PageBase):
    """
    This class contains the elements of login page.
    """

    def __init__(self, py):
        super().__init__(py)
        self.py = py

    @property
    def username_field(self) -> Element:
        """
        :return: element
        """
        locator = "[type='email']"
        element = self.py.get(locator)
        return element

    @property
    def password_field(self) -> Element:
        """
        :return: element
        """
        locator = "[type='password']"
        element = self.py.get(locator)
        return element

    @property
    def login_button(self) -> Element:
        """
        :return: element
        """
        locator = ".item>button"
        element = self.py.get(locator)
        return element

    def login(self, username, password):
        """
        This function used to login.
        :param username: String
        :param password: String
        """
        self.username_field.type(username)
        self.password_field.type(password)
        self.login_button.should().be_enabled()
        self.login_button.click()
        current_wait = 10
        if "login" in self.py.url():
            self.artifacts.logger.info(f"Current wait time to login is set to {current_wait} seconds")
            self.py.wait(current_wait).until(ec.url_contains("dashboard"))
