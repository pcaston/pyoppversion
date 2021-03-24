"""Fixtures."""
import pytest


@pytest.fixture()
def oppio_response():
    """Response when no active beta"""
    return {
        "supervisor": "999",
        "openpeerpower": {"default": "9.99.9"},
        "oppos": {"ova": "9.99"},
        "cli": "9",
    }


@pytest.fixture()
def oppio_beta_response():
    """Beta response when no beta during beta week."""
    return {
        "supervisor": "999",
        "openpeerpower": {"default": "9.99.9"},
        "oppos": {"ova": "9.99"},
        "cli": "9",
    }


@pytest.fixture()
def oppio_response_beta_week():
    """Response when active beta during beta week."""
    return {
        "supervisor": "999",
        "openpeerpower": {"default": "9.98.9"},
        "oppos": {"ova": "9.99"},
        "cli": "9",
    }


@pytest.fixture()
def oppio_beta_response_beta_week():
    """Beta response when active beta during beta week."""
    return {
        "supervisor": "999",
        "openpeerpower": {"default": "9.99.9b0"},
        "oppos": {"ova": "9.99"},
        "cli": "9",
    }
