import secrets
from typing import Any, Dict
from fastapi import FastAPI, Response, status
from pydantic import BaseModel


class Signature(BaseModel):
    signature: str


class Signed(Signature):
    data: dict[str, Any]


def _encode(value: Dict) -> str:
    return ""


def _decode(value: Dict) -> str:
    return ""


def _sign(payload: Dict, secret: bytes) -> Signature:
    return Signature(signature="")


def _verify(signed: Signed, secret: bytes) -> bool:
    return _sign(signed.data, secret).signature == signed.signature


def setup():
    # TODO: Setup environment variable.
    static_secret = secrets.token_bytes(32)
    app = FastAPI()

    @app.post("/encrypt")
    def encrypt(payload: Dict):
        return _encode(payload)

    @app.post("/decrypt")
    def decrypt(payload: Dict):
        return _decode(payload)

    @app.post("/sign")
    def sign(payload: Dict):
        return _sign(payload, static_secret)

    @app.post("/verify")
    def verify(signed: Signed):
        if _verify(signed, static_secret):
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status_code=status.HTTP_400_BAD_REQUEST)

    return app
