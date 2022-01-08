import json
import tempfile
from pathlib import Path

import pytest

from pynata.utils import json_to_dict

DATA = {"test": "foobar"}


@pytest.fixture
def temp_json_path():
    with tempfile.TemporaryDirectory() as temp_dir:
        path = Path(temp_dir) / "test_file.json"
        path.write_text(json.dumps(DATA))
        yield path


@pytest.fixture
def temp_json_file(temp_json_path):
    with open(str(temp_json_path)) as temp_file:
        yield temp_file


def test_json_to_dict_when_path(temp_json_path):
    actual = json_to_dict(temp_json_path)
    expected = DATA
    assert actual == expected


def test_json_to_dict_when_file(temp_json_file):
    actual = json_to_dict(temp_json_file)
    expected = DATA
    assert actual == expected


def test_json_to_dict_when_dict(temp_json_file):
    actual = json_to_dict(DATA)
    expected = DATA
    assert actual == expected
