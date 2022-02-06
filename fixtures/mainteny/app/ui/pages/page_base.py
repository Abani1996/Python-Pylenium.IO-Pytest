"""
Page Base Module
"""
from fixtures.harness.artifacts import HarnessArtifacts as Artifacts


class PageBase:
    """
    This base class contains generic objects.
    """

    def __init__(self, py):
        self.py = py
        self.artifacts = Artifacts()
