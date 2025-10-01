
from typing import Any, Callable, Dict

from pydantic import BaseModel


type Payload = Dict[str, Any]
type EncodedPayload = Dict[str, str]
type Encoder = Callable[[Any], bytes]
type Decoder = Callable[[bytes], Any]
type Signer = Callable[[Payload, bytes], Signature]


class Signature(BaseModel):
    signature: str


class Signed(Signature):
    data: Payload

