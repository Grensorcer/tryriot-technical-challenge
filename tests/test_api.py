from context import api, examples, non_encoded_examples
from cryptography import base64
from fastapi import status
from fastapi.testclient import TestClient
from faker import Faker

app = api.setup()
client = TestClient(app)

routes = ["/encrypt", "/decrypt", "/sign", "/verify"]


def check_bad_input(route, **kwargs):
    assert (
        client.post(route, **kwargs).status_code
        == status.HTTP_422_UNPROCESSABLE_CONTENT
    )


def check_good_input(route, expected, **kwargs):
    response = client.post(route, **kwargs)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected


def test_wrong_method():
    response = client.get("/decrypt")
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    response = client.get("/encrypt")
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    response = client.get("/sign")
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    response = client.get("/verify")
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_wrong_input():
    for route in routes:
        check_bad_input(route, json="blbl")
        check_bad_input(route, json=True)
        check_bad_input(route, json=34)
        check_bad_input(route, json=None)
        check_bad_input(route, json="")

        check_bad_input(
            route, content="a", headers={"Content-Type": "application/json"}
        )
        check_bad_input(
            route, content="134", headers={"Content-Type": "application/json"}
        )
        check_bad_input(
            route, content="true", headers={"Content-Type": "application/json"}
        )
        check_bad_input(
            route, content="True", headers={"Content-Type": "application/json"}
        )
        check_bad_input(route, content="", headers={"Content-Type": "application/json"})
        check_bad_input(
            route, content="{ a }", headers={"Content-Type": "application/json"}
        )
        check_bad_input(
            route, content='{ "a": b }', headers={"Content-Type": "application/json"}
        )
        check_bad_input(
            route, content="<>", headers={"Content-Type": "application/xml"}
        )


methods = [[base64.encode, base64.decode]]


def test_encode_examples():
    for [encode, _] in methods:
        for [b64, og] in examples:
            assert api._encode(og, encode) == b64


def test_decode_examples():
    for [_, decode] in methods:
        for [b64, og] in examples:
            assert api._decode(b64, decode) == og


def test_decode_nonencoded():
    for [_, decode] in methods:
        for [b64, og] in non_encoded_examples:
            assert api._decode(b64, decode) == og


def test_encode_decode():
    for [encode, decode] in methods:
        _encode = lambda x: api._encode(x, encode)
        _decode = lambda x: api._decode(x, decode)

        def test(og, b64):
            assert _decode(_encode(og)) == og
            assert _encode(_decode(b64)) == b64

        for [b64, og] in examples:
            test(og, b64)


def test_random_json():
    fake = Faker()
    data = [
        fake.pydict(
            5,
            True,
            value_types=[str, int, float, bool],
            allowed_types=[str, int, float, bool],
        )
        for _ in range(1000)
    ]
    for j in data:
        response = client.post("/encrypt", json=j)
        assert response.status_code == status.HTTP_200_OK

        encrypted = response.json()
        response = client.post("/decrypt", json=encrypted)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == j

        response = client.post("/sign", json=j)
        assert response.status_code == status.HTTP_200_OK
        response = client.post("/verify", json={ "data": j, **response.json()})
        assert response.status_code == status.HTTP_204_NO_CONTENT