import json
from os import walk
from os.path import isfile

import requests


_MAPPINGS_DIR = "tests/data/mock_api"


def setup_mock(api_host: str) -> None:
    mappings_url = f"{api_host}/__admin/mappings"
    for dirpath, dirnames, filenames in walk(_MAPPINGS_DIR):
        for mock_spec in filenames:
            filename = f"{dirpath}/{mock_spec}"
            if not isfile(filename):
                continue
            with open(filename, "r") as spec_file:
                spec = json.loads(spec_file.read())
                requests.post(url=mappings_url, json=spec)
