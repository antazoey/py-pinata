from pathlib import Path
from typing import List, Optional

from nft_utils import Pin, PinningAPI

from pynata.api_key import get_key_manager
from pynata.clients.data import DataClient
from pynata.clients.pinning import PinningClient
from pynata.exceptions import (
    NoContentError,
    PinataBadRequestError,
    PinataInternalServiceError,
    PinError,
)
from pynata.session import PinataAPISession


class Pinata(PinningAPI):
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

    def get_pins(self) -> List[Pin]:
        pins = self.data.search_pins(status="pinned")["rows"]
        return [
            Pin(content_hash=p["ipfs_pin_hash"], file_name=p["metadata"]["name"])
            for p in pins
        ]

    def get_hash(self, artwork_name: str) -> Optional[str]:
        pins = self.get_pins()
        for pin in pins:
            if pin.file_name == artwork_name:
                return pin.content_hash

        return None

    def pin_file(self, file_path: Path) -> str:
        """
        Add and pin any file, or directory, to Pinata's IPFS nodes.

        Args:
            file_path (pathlib.Path): The path to the file to pin.

        Returns:
            :class:`~pynata.response.PinataResponse`
        """

        is_json = file_path.suffix == ".json"
        try:
            response = (
                self.pinning.pin_json(file_path)
                if is_json
                else self.pinning.pin_file(file_path)
            )
        except PinataBadRequestError as err:
            raise PinError(file_path) from err

        return response.data["IpfsHash"]

    def unpin(self, content_hash: str):
        """
        Unpin content they previously uploaded to Pinata's IPFS nodes.

        Args:
            content_hash (str): The hash of the content to stop pinning.

        Returns:
            :class:`~pynata.response.PinataResponse`
        """
        try:
            self.pinning.unpin(content_hash)
        except PinataInternalServiceError as err:
            raise NoContentError(content_hash) from err
