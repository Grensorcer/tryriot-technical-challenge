from context import api
from fastapi import status
from fastapi.testclient import TestClient

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

        check_bad_input(route, content="a", headers={"Content-Type": "application/json"})
        check_bad_input(route, content="134", headers={"Content-Type": "application/json"})
        check_bad_input(route, content="true", headers={"Content-Type": "application/json"})
        check_bad_input(route, content="True", headers={"Content-Type": "application/json"})
        check_bad_input(route, content="", headers={"Content-Type": "application/json"})
        check_bad_input(route, content="{ a }", headers={"Content-Type": "application/json"})
        check_bad_input(route, content='{ "a": b }', headers={"Content-Type": "application/json"})
        check_bad_input(route, content="<>", headers={"Content-Type": "application/xml"})
