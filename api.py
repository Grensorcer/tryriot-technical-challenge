from api_types import (
    Decoder,
    EncodedPayload,
    Encoder,
    Payload,
    Signature,
    Signed,
    Signer,
)
from cryptography import base64, hmac
import secrets
from fastapi import FastAPI, Response, status


def _encode(payload: Payload, method: Encoder) -> EncodedPayload:
    return {key: method(val).decode() for key, val in payload.items()}


def _decode(payload: EncodedPayload, method: Decoder) -> Payload:
    def f(value):
        decoded = method(value)
        return decoded if decoded is not None else value.decode()

    return {key: f(val.encode()) for key, val in payload.items()}


def _sign(payload: Payload, secret: bytes, method: Signer) -> Signature:
    return method(payload, secret)


def _verify(signed: Signed, secret: bytes, method: Signer) -> bool:
    return _sign(signed.data, secret, method).signature == signed.signature


def setup():
    # TODO: Setup environment variable.
    static_secret = secrets.token_bytes(32)
    app = FastAPI()

    @app.post("/encrypt")
    def encrypt(payload: Payload):
        return _encode(payload, base64.encode)

    @app.post("/decrypt")
    def decrypt(payload: EncodedPayload):
        return _decode(payload, base64.decode)

    @app.post("/sign")
    def sign(payload: Payload):
        return _sign(payload, static_secret, hmac.hmac256)

    @app.post("/verify", responses={204: {}, 400: {}})
    def verify(signed: Signed, response: Response):
        if _verify(signed, static_secret, hmac.hmac256):
            response.status_code = status.HTTP_204_NO_CONTENT
        else:
            response.status_code = status.HTTP_400_BAD_REQUEST
        return

    return app
