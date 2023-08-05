"""
Test Init module.

This module contains tests for project init.
"""
import pytest

from Simyan import api, exceptions, session


def test_api():
    """Test for api()."""
    with pytest.raises(exceptions.AuthenticationError):
        api()

    m = None
    try:
        m = api(api_key="Something")
    except Exception as exc:
        print(f"Simyan.api() raised {exc} unexpectedly!")

    assert m.__class__.__name__ == session.Session.__name__
