# tryriot-technical-challenge

This repository contains a REST API implementing the endpoints described in [Riot's technical challenge](https://github.com/tryriot/take-home)

## Requirements

* Python 3.13

## Configuration

The server will look for an environment variable *SECRET_TOKEN* or a *.env* file defining it which will be used as the signature encryption key.
In case this variable is not found, a 32B token will be generated and discarded on server shutdown.

### CLI secret generation command example

`head -c 32 /dev/random | xxd -c 32 -ps`

## Dockerfile

A Dockerfile is available with 3 pre-defined targets
* **prod** builds an image ready to run the production server on port 80
* **dev** builds an image ready to run the development server on port 80
* **test** builds and runs tests

**prod** and **dev** targets can be configured with the *SECRET_TOKEN* environment variable.
This Dockerfile was tested with Docker and Podman.

### Example

Building and running the production server with a generated token would look like:
* `docker build -t <image_name> --progress=plain --target=prod .`
* `SECRET=$(head -c 32 /dev/random | xxd -c 32 -ps); docker run --rm -e SECRET_TOKEN=$SECRET -d -p 8080:80 <image_name>`

Building and running tests with a generated token would look like:
* `SECRET=$(head -c 32 /dev/random | xxd -c 32 -ps); docker build -t <image_name> --env SECRET_TOKEN=$SECRET --target=test --no-cache .`

## Local installation

1. Create a virtual environment `python3 -m venv .venv`
2. Activate the virtual environment `source .venv/bin/activate`
3. Install the dependencies `pip install -r requirements.txt`

### Mise

If you are a Mise user, you may simply run `mise trust && mise install && mise run install` to set up a virtual environment using the right Python version and install its dependencies.

## Running

1. Using fastapi (installed in the requirements.txt file), run `fastapi run main.py` to start the production server. Replace `run` with `dev` for the development server.
2. Tests may be run using pytest by running: `pytest`

### Mise

Using mise, multiple tasks are set up in *mise.toml* to start the server and run tests.