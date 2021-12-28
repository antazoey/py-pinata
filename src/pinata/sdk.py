from pathlib import Path

from pinata.api_key import get_key_manager
from pinata.clients.data import DataClient
from pinata.clients.pinning import PinningClient
from pinata.exceptions import PinataInternalServiceError, NoContentError
from pinata.logger import logger
from pinata.response import PinataResponse
from pinata.session import PinataAPISession


class Pinata:
    def __init__(self, pinning_client: PinningClient, data_client: DataClient):
        self.pinning = pinning_client
        self.data = data_client

    @classmethod
    def from_profile_name(cls, profile_name: str) -> "Pinata":
        """
        Create an instance of the Pinata SDK from a stored profile name.

        Args:
            profile_name (str): The name of the API key profile to use.
        """
        key_manager = get_key_manager()
        api_key, api_secret = key_manager.get_key_pair(profile_name)
        return cls.from_api_key(api_key, api_secret)

    @classmethod
    def from_api_key(cls, api_key: str, api_secret: str) -> "Pinata":
        """
        Create an instance of the Pinata SDK from an API key.
        `Guide on API key <https://docs.pinata.cloud/user/generate-api-key>`__.

        Args:
            api_key (str): The API key.
            api_secret (str): The API secret.
        """
        session = PinataAPISession.from_api_key(api_key, api_secret)
        pinning_client = PinningClient(session)
        data_client = DataClient(session)
        return cls(pinning_client, data_client)

    def pin_file(self, file_path: Path) -> PinataResponse:
        """
        Add and pin any file, or directory, to Pinata's IPFS nodes.

        Args:
            file_path (pathlib.Path): The path to the file to pin.

        Returns:
            :class:`~pinata.response.PinataResponse`
        """

        return self.pinning.pin_file(file_path)

    def pin_json(self, json_file_path: Path) -> PinataResponse:
        """
        Add and pin any JSON object they wish to Pinata's IPFS nodes. This endpoint is
        specifically optimized to only handle JSON content.

        Args:
            json_file_path (pathlib.Path): The path to a JSON file.

        Returns:
            :class:`~pinata.response.PinataResponse`
        """

        return self.pinning.pin_json(json_file_path)

    def unpin(self, content_hash: str) -> PinataResponse:
        """
        Unpin content they previously uploaded to Pinata's IPFS nodes.

        Args:
            content_hash (str): The hash of the content to stop pinning.

        Returns:
            :class:`~pinata.response.PinataResponse`
        """
        try:
            return self.pinning.unpin(content_hash)
        except PinataInternalServiceError as err:
            raise NoContentError(content_hash) from err
