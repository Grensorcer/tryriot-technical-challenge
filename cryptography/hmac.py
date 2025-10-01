from hmac import HMAC
from api_types import Payload, Signature
from cryptography import base64


def hmac256(payload: Payload, secret: bytes):
    return Signature(
        signature=HMAC(secret, base64.encode(payload), "sha256").hexdigest()
    )
