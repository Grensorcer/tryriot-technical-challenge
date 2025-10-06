FROM python:3.13 as base
WORKDIR /source
COPY ./requirements.txt ./requirements.txt
RUN pip install --root-user-action ignore --no-cache-dir --upgrade -r ./requirements.txt
COPY ./*.py ./
COPY ./cryptography ./cryptography

FROM base as test
COPY ./tests ./tests
RUN pytest

FROM base as dev
CMD ["fastapi", "dev", "main.py", "--host", "0.0.0.0", "--port", "80"]

FROM base as prod
CMD ["fastapi", "run", "main.py", "--port", "80"]

