# Vantage - Developer README

Welcome to the Vantage project! This document provides all the necessary instructions to get you set up and running.

## Environment Setup

### Prerequisites

Before you begin, ensure you have the following installed:
- [Poetry](https://python-poetry.org/)
- [pyenv](https://github.com/pyenv/pyenv)


### Setting up `Poetry`

`Poetry` is a tool for dependency management and packaging in Python.

1. Install `Poetry` (1.7.1) using the instructions provided [here](https://python-poetry.org/docs/#installation).

### Setting up `pyenv`

`pyenv` is a Python version management tool. It allows you to install multiple versions of Python and easily switch between them.

1. Install `pyenv` following the instructions [here](https://github.com/pyenv/pyenv#installation).
2. Install the Python version used in Vantage project (e.g., Python 3.10.13):
   ```sh
   pyenv install 3.10.13
   ```
3. Create virtual environment using pyenv and installed Python version:
    ```sh
    pyenv virtualenv 3.10.13 vantage-sdk-env
    ```
4. Activate created virtual environment:
    ```sh
    pyenv activate vantage-sdk-env
    ```

## Installation

### Getting the codebase

- Clone the repository:
  ```sh
  git clone git@github.com:VantageDiscovery/vantage-sdk-python.git
  ```

- Navigate to the cloned directory:
    ```sh
    cd vantage-sdk-python
    ```

### Installing the package

- Inside the activated virtual environment, install the dependencies:
   ```sh
   poetry install --all-extras
   ```

- Then run the following command to install Vantage library locally:
    ```sh
    python -m pip install .
    ```

## Vantage SDK Usage

Now that the Vantage library is installed, you're almost ready to use it. All you need to do is set up the necessary environment variables:

```sh
export VANTAGE_API_KEY=<YOUR_VANTAGE_API_KEY>
export VANTAGE_API_CLIENT_ID=<YOUR_VANTAGE_CLIENT_ID>
export VANTAGE_API_CLIENT_SECRET=<YOUR_VANTAGE_CLIENT_SECRET>
```

Once that's done, you can run the following script to get started:

```python
import os
from pprint import pprint

from vantage import Vantage

vantage_instance = Vantage.from_defaults(
    vantage_client_id=os.environ["VANTAGE_API_CLIENT_ID"],
    vantage_client_secret=os.environ["YOUR_VANTAGE_CLIENT_SECRET"],
)

res = vantage_instance.logged_in_user()

pprint(res)
```

Feel free to check `/examples` directory for some more detailed examples.
