from context import examples, non_encoded_examples
from cryptography.base64 import encode, decode

values = [
    ["bnVsbA==", None],
    ["dHJ1ZQ==", True],
    ["", ""],
    ["IiI=", '""'],
    ["aGVsbG8=", "hello"],
    ["Sm9obiBEb2U=", "John Doe"],
    ["MzA=", 30],
    ["W10=", []],
    ["WzEsMiwzXQ==", [1, 2, 3]],
    ["e30=", {}],
    ["eyJudWxsIjpudWxsLCJ0cnVlIjp0cnVlfQ==", {"null": None, "true": True}],
    [
        "eyJlbWFpbCI6ImpvaG5AZXhhbXBsZS5jb20iLCJwaG9uZSI6IjEyMy00NTYtNzg5MCJ9",
        {"email": "john@example.com", "phone": "123-456-7890"},
    ],
]

non_encoded = [
    "a",
    "lasdlasdasl"
    "Hello there",
    "123"
]

def test_encode_values_b64():
    for [b64, og] in values:
        assert encode(og).decode() == b64


def test_decode_values_b64():
    for [b64, og] in values:
        assert decode(b64) == og


def test_decode_nonencoded():
    for b64 in non_encoded:
        assert decode(b64) is None


def test_encode_decode():
    def test(og, b64):
        assert decode(encode(og)) == og
        assert encode(decode(b64)).decode() == b64

    for [b64, og] in values:
        test(og, b64)
