import pytest
from click.testing import CliRunner

from pinata.api_key import KeyringManager
from pinata.cli import cli
from pinata.clients.data import DataClient
from pinata.sdk import Pinata

MOCK_FILE_NAME_1 = "MOCK_FILE_1.jpeg"
MOCK_FILE_NAME_2 = "MOCK_FILE_2.jpeg"

MOCK_PIN_HASH_1 = "MOCK_PIN_HASH_1"
MOCK_PIN_HASH_2 = "MOCK_PIN_HASH_2"

MOCK_PIN_DATE_1 = "2020-02-08T09:30:26.123Z"
MOCK_PIN_DATE_2 = "2020-01-05T04:24:21.234Z"

MOCK_API_KEY = "MOCK_API_KEY"
MOCK_API_SECRET = "MOCK_API_SECRET"


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def root_cli():
    return cli


@pytest.fixture(autouse=True)
def mock_keys(mocker):
    mock = mocker.MagicMock(spec=KeyringManager)
    mock.get_key_pair.return_value = (MOCK_API_KEY, MOCK_API_SECRET)
    patch = mocker.patch("pinata.cli.get_key_manager")
    patch.return_value = mock
    return mock


@pytest.fixture(autouse=True)
def mock_data_client(mocker):
    return mocker.MagicMock(spec=DataClient)


@pytest.fixture(autouse=True)
def mock_pinata(mocker, mock_data_client):
    mock = mocker.MagicMock(spec=Pinata)
    mock.data = mock_data_client
    patch = mocker.patch("pinata.cli.Pinata.from_api_key")
    patch.return_value = mock
    return mock


@pytest.fixture
def pins_data():
    return {
        "rows": [
            {
                "ipfs_pin_hash": MOCK_PIN_HASH_1,
                "date_pinned": MOCK_PIN_DATE_1,
                "metadata": {"name": MOCK_FILE_NAME_1},
            },
            {
                "ipfs_pin_hash": MOCK_PIN_HASH_2,
                "date_pinned": MOCK_PIN_DATE_2,
                "metadata": {"name": MOCK_FILE_NAME_2},
            },
        ]
    }
