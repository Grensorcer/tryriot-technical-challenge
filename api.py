from cryptography import base64
import secrets
from typing import Any, Callable, Dict
from fastapi import FastAPI, Response, status
from pydantic import BaseModel

type Payload = Dict[str, Any]
type EncodedPayload = Dict[str, str]
type Encoder = Callable[[Any], bytes]
type Decoder = Callable[[bytes], Any]


class Signature(BaseModel):
    signature: str


class Signed(Signature):
    data: Payload


def _encode(payload: Payload, method: Encoder) -> EncodedPayload:
    return { key: method(val).decode() for key, val in payload.items() }


def _decode(payload: EncodedPayload, method: Decoder) -> Payload:
    def f(value):
        decoded = method(value)
        return decoded if decoded is not None else value.decode()
    return { key: f(val.encode()) for key, val in payload.items() }


def _sign(payload: Payload, secret: bytes) -> Signature:
    return Signature(signature="")


def _verify(signed: Signed, secret: bytes) -> bool:
    return _sign(signed.data, secret).signature == signed.signature


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
        return _sign(payload, static_secret)

    @app.post("/verify", responses={204: {}, 400: {}})
    def verify(signed: Signed, response: Response):
        if _verify(signed, static_secret):
            response.status_code = status.HTTP_204_NO_CONTENT
        else:
            response.status_code = status.HTTP_400_BAD_REQUEST
        return

    return app
