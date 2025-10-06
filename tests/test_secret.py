import os
from cryptography.secret import get_or_create_secret
from dotenv import load_dotenv, set_key

def test_reuse_secret():
    name = "SECRET_TOKEN"
    secret = get_or_create_secret(name)
    assert secret == get_or_create_secret(name)
    assert secret != get_or_create_secret("TEST")


def test_load_secret():
    path = ".env.test"
    name = "SECRET_TOKEN"
    secret = get_or_create_secret(name)
    set_key(path, key_to_set=name, value_to_set=secret.decode())
    os.environ.pop(name)

    load_dotenv(path)
    assert secret.decode() == os.environ[name]
    assert secret == get_or_create_secret(name)
    assert secret != get_or_create_secret("TEST")
