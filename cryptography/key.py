import os
import secrets
from dotenv import set_key


def get_or_create_key(n: int) -> bytes:
    """
    Generate a random key of length n and store it in the environment,
    or get it if it already exists.

    @param n: The length of the key to generate.
    @return: The key as bytes.
    """
    name = f"KEY_{n}"
    if name in os.environ:
        return os.environ[name].encode()
    else:
        key = secrets.token_hex(n)  # Using n bytes
        os.environ[name] = key
        set_key(".env", key_to_set=name, value_to_set=key)
        return key.encode()
