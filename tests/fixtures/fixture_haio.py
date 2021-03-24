"""Fixtures."""
import pytest


@pytest.fixture()
def oppio_response():
    """Response for https://www.openpeerpower.io//version.json."""
    return {"current_version": "9.99.9"}
