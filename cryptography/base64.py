from base64 import b64encode, b64decode
import binascii
import json
from typing import Any


def encode(value: Any)-> bytes:
    if not isinstance(value, str):
        value = json.dumps(value, separators=(",", ":"), sort_keys=True)
    return b64encode(value.encode())


def decode(value: bytes) -> Any:
    try:
        res = b64decode(value, validate=True).decode()
    except binascii.Error as err:
        print(f"[decode][base64] error: {err}")
        return None

    try:
        return res if res.startswith('"') and res.endswith('"') else json.loads(res)
    except json.JSONDecodeError:
        return res

    print("[decode][base64] unknown error")
    return None
