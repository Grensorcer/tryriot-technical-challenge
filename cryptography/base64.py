from base64 import b64encode, b64decode
import binascii
import json
from typing import Any


def encode(value: Any)-> bytes:
    """
    Encode any json-serializable value to base64 encoded string.
    Handle string ambiguity with `json.dumps` 

    @param value: any json-serializable value
    @return: base64 encoded string
    """
    if not isinstance(value, str):
        value = json.dumps(value, separators=(",", ":"), sort_keys=True)
    return b64encode(value.encode())


def decode(value: bytes) -> Any | None:
    """
    Decode base64 encoded json string.
    Handle string ambiguity with `json.loads`

    @param value: base64 encoded json string
    @return: decoded json object or None on failure
    """
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
