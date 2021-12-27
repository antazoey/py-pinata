from pinata.clients.data import DataClient
from pinata.clients.pinning import PinningClient
from pinata.session import PinataAPISession
from pinata.api_key import get_key_manager


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
