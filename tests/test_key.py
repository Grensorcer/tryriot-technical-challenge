import os
from cryptography.key import get_or_create_key
from dotenv import load_dotenv, set_key

def test_reuse_key():
    key = get_or_create_key(32)
    assert key == get_or_create_key(32)
    assert key != get_or_create_key(16)
    assert key != get_or_create_key(64)

def test_persist_key():
    path = ".env.test"
    size = 32
    name = f"KEY_{size}"
    key = get_or_create_key(size)
    set_key(path, key_to_set="KEY_32", value_to_set=key.decode())
    os.environ[name] = ""

    load_dotenv(path)
    key == get_or_create_key(size)