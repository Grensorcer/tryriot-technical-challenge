from hmac import HMAC
from api_types import Payload, Signature
from cryptography import base64


def hmac256(payload: Payload, secret: bytes):
    """
    Generates a HMAC256 signature string for the given payload and secret. 

    @param payload: The payload to sign.
    @param secret: The secret key used for signing.
    @return: A Signature object containing the HMAC256 signature.
    """
    return Signature(
        signature=HMAC(secret, base64.encode(payload), "sha256").hexdigest()
    )
