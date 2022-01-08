# py-pinata

A python wrapper around the Pinata REST APIs

# Initialize the SDK

One way to initialize the SDK is by saving and using your API key and secret using
[keyring](https://pypi.org/project/keyring/).

```python
import keyring
from pynata import Pinata

# Save your API key + secret in 'keyring'.
keyring.set_password("pynata", "api-key", "MY_API_KEY")
keyring.set_password("pynata", "api-secret", "MY_API_SECRET")

# Access your secrets when initializing the Pinata SDK.
api_key = keyring.get_password("pynata", "api-key")
api_secret = keyring.get_password("pynata", "api-secret")

# Use the classmethod 'from_api_key()' to create an instance of Pinata.
sdk = Pinata.from_api_key(api_key, api_secret)
```

You can also use the CLI to import an API key:

```bash
pinata api-key import <PROFILE_NAME>
```

## Query Pins

Once you have an SDK, you can use it to query your pins:

```python
response = sdk.data.search_pins(status=status)
pins = response["rows"]
for pin in pins:
    ipfs_hash = pin['ipfs_pin_hash']
    print(ipfs_hash)
```

You can also use the CLI:

```bash
pinata list-pins
```

## Pin Files

Pin new files to IPFS:

```python
ipfs_hash = pinata.pin_file("path/to/file")
```
