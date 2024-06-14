import json
import os
from os import walk
from os.path import isfile
from typing import Any

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


def get_mock_request_for(module_name: str, test_name: str) -> dict[str, Any]:
    filename = f"{_MAPPINGS_DIR}/{module_name}-{test_name}.json"
    with open(filename) as json_file:
        return json.loads(json_file.read())


def get_request_stub_file_contents(request: Any) -> dict[str, Any]:
    try:
        test_name = request.node.name
        module_name = os.path.basename(request.path).replace(".py", "")

        return get_mock_request_for(module_name, test_name)
    except Exception as exception:
        raise exception
