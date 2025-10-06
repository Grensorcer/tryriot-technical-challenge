import os
import secrets

def create_secret(n: int) -> str:
    return secrets.token_hex(n)


def get_or_create_secret(name: str) -> bytes:
    """
    Generate a random key of length n and store it in the environment,
    or get it if it already exists.

    @param n: The length of the key to generate.
    @return: The key as bytes.
    """
    if name in os.environ:
        return os.environ[name].encode()
    else:
        DEFAULT_KEY_SIZE = 32
        secret = create_secret(DEFAULT_KEY_SIZE)
        os.environ[name] = secret # Set key in environment
        return secret.encode()
