"""
DashboardPage Module
"""

from fixtures.mainteny.app.ui.pages.page_base import PageBase
from pylenium.element import Element


class DashboardPage(PageBase):
    """
    This class contains the elements of Dashboard page.
    """
    def __init__(self, py):
        super().__init__(py)
        self.py = py

    @property
    def pending_orders(self) -> Element:
        """
        :return: element
        """
        locator = "div.status-tile.pending-status.col .value"
        element = self.py.get(locator)
        return element
