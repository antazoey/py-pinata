from pynata.utils import prettify_date

from .conftest import (
    MOCK_FILE_NAME_1,
    MOCK_FILE_NAME_2,
    MOCK_PIN_DATE_1,
    MOCK_PIN_DATE_2,
    MOCK_PIN_HASH_1,
    MOCK_PIN_HASH_2,
)


def test_list_pins(runner, root_cli, mock_data_client, pins_data):
    mock_data_client.search_pins.return_value = pins_data

    result = runner.invoke(root_cli, ["list-pins"])

    if result.exception:
        raise result.exception

    expected_date_1 = prettify_date(MOCK_PIN_DATE_1)
    expected_date_2 = prettify_date(MOCK_PIN_DATE_2)
    assert result.exit_code == 0, result.output
    assert MOCK_FILE_NAME_1 in result.output
    assert MOCK_FILE_NAME_2 in result.output
    assert MOCK_PIN_HASH_1 in result.output
    assert MOCK_PIN_HASH_2 in result.output
    assert expected_date_1 in result.output
    assert expected_date_2 in result.output
