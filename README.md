# tryriot-technical-challenge

This repository contains a REST API implementing the endpoints described in [Riot's technical challenge](https://github.com/tryriot/take-home)

## Requirements

* Python 3.13

## Installation

1. Clone the repository.
2. Create a virtual environment `python3 -m venv .venv`
3. Activate the virtual environment `source .venv/bin/activate`
4. Install the dependencies `pip install -r requirements.txt`

### Mise

If you are a Mise user, you may simply run `mise trust && mise install && mise run install` to set up a virtual environment using the right Python version and install its dependencies.

## Running

1. Using fastapi (installed in the requirements.txt file), run `fastapi run main.py` to start the production server. Replace `run` with `dev` for the development server.
2. Tests may be run using pytest by running: `pytest`

### Mise

Using mise, multiple tasks are set up in mise.toml to start the server and run tests.