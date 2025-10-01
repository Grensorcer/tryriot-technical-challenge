import secrets
from cryptography.hmac import hmac256

example = {"message": "Hello World", "timestamp": 1616161616}
revert_example = {"timestamp": 1616161616, "message": "Hello World"}
tampered_data = {"timestamp": 1616161616, "message": "Goodbye World"}


def test_sign():
    secret = secrets.token_bytes(32)
    assert hmac256(example, secret).signature == hmac256(revert_example, secret).signature
    assert hmac256(example, secret).signature != hmac256(tampered_data, secret).signature