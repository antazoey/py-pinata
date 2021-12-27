from pathlib import Path

from pinata.clients.data import DataClient
from pinata.clients.pinning import PinningClient
from pinata.session import PinataAPISession


class Pinata:
    def __init__(self, pinning_client: PinningClient, data_client: DataClient):
        self.pinning = pinning_client
        self.data = data_client

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
