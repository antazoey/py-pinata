from pynata.sdk import Pinata
from pynata.api_key import set_keys_from_prompt


def create_pinata(profile_name: str) -> Pinata:
    """
    Get or create a Pinata SDK instance with the given profile name.
    If the profile does not exist, you will be prompted to create one,
    which means you will be prompted for your API key and secret. After
    that, they will be stored securely using ``keyring`` and accessed
    as needed without prompt.

    Args:
        profile_name (str): The name of the profile to get or create.

    Returns:
        :class:`~pynata.sdk.Pinata`
    """

    pinata = Pinata.from_profile_name(profile_name)
    if not pinata:
        set_keys_from_prompt(profile_name)

    return Pinata.from_profile_name(profile_name)


__all__ = ["Pinata", "create_pinata"]
