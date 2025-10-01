import os
import sys
from typing import List, Tuple

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import api

examples: List[Tuple[api.EncodedPayload, api.Payload]] = [
    [
        {"email": "am9obkBleGFtcGxlLmNvbQ==", "phone": "MTIzLTQ1Ni03ODkw"},
        {"email": "john@example.com", "phone": "123-456-7890"},
    ],
    [
        {
            "name": "Sm9obiBEb2U=",
            "age": "MzA=",
            "contact": "eyJlbWFpbCI6ImpvaG5AZXhhbXBsZS5jb20iLCJwaG9uZSI6IjEyMy00NTYtNzg5MCJ9",
        },
        {
            "name": "John Doe",
            "age": 30,
            "contact": {"email": "john@example.com", "phone": "123-456-7890"},
        },
    ],
]

non_encoded_examples: List[Tuple[api.EncodedPayload, api.Payload]] = [
    [
        {
            "name": "Sm9obiBEb2U=",
            "age": "MzA=",
            "contact": "eyJlbWFpbCI6ImpvaG5AZXhhbXBsZS5jb20iLCJwaG9uZSI6IjEyMy00NTYtNzg5MCJ9",
            "birth_date": "1998-11-19",
        },
        {
            "name": "John Doe",
            "age": 30,
            "contact": {"email": "john@example.com", "phone": "123-456-7890"},
            "birth_date": "1998-11-19",
        },
    ]
]
