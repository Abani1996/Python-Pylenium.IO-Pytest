"""
Fixtures and functions to handle test artifacts
"""


import logging
import pytest


class HarnessArtifacts:
    """Artifact object to handle logging and other artifacts"""

    def __init__(self):
        self.logger = logging.getLogger("test_log")


@pytest.fixture(scope="session", name="artifacts")
def fixture_artifacts():
    """Returns HarnessArtifacts class"""
    ha = HarnessArtifacts()
    return ha
