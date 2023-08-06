import pathlib

import pytest


@pytest.fixture()
def data_fixtures():
    """Load a data fixture."""
    return pathlib.Path(__file__).parent / "test_data"
