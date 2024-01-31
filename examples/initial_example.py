"""
[WIP]
Initial example of the Vantage Python SDK Usage.
Please set your ACCOUNT_ID and environment variables accordingly.
"""

import os
from argparse import ArgumentParser
from pprint import pprint

from vantage import Vantage


ACCOUNT_ID = "<YOUR_ACCOUNT_ID>"
EXTERNAL_KEY_ID = "<YOUR_EXTERNAL_KEY_ID>"
VANTAGE_API_KEY = "<YOUR_VANTAGE_API_KEY>"
DEFAULT_JWT_TOKEN = None

DEFAULT_TASK = "list_collections"
DEFAULT_COLLECTION_ID = "test-sdk"
DEFAULT_COLLECTION_NAME = "Test SDK"
DEFAULT_UPDATE_COLLECTION_NAME = "New Test SDK Name"

USER_PROVIDED_EMBEDDINGS = False
DEFAULT_LLM = "text-embedding-ada-002"
DEFAULT_LLM_EMBEDDINGS_DIM = 1536

DEFAULT_QUERY_TEXT = "some query"

DEFAULT_API_HOST = "https://api.dev-a.dev.vantagediscovery.com"
DEFAULT_AUTH_HOST = "https://vantage-dev.us.auth0.com"


def main(
    task: str, collection_id: str, file_path: str, query_text: str
) -> None:
    jwt_token = os.getenv("VANTAGE_API_JWT_TOKEN")
    if jwt_token is None:
        vantage_instance = Vantage.using_client_credentials(
            vantage_client_id=os.environ["VANTAGE_API_CLIENT_ID"],
            vantage_client_secret=os.environ["VANTAGE_API_CLIENT_SECRET"],
            account_id=ACCOUNT_ID,
            api_host=DEFAULT_API_HOST,
            auth_host=DEFAULT_AUTH_HOST,
        )
    else:
        vantage_instance = Vantage.using_jwt_token(
            vantage_api_jwt_token=jwt_token,
            api_host=DEFAULT_API_HOST,
            account_id=ACCOUNT_ID,
        )

    if task == "vantage_keys":
        keys = vantage_instance.get_vantage_api_keys()
        res = [key.actual_instance.dict() for key in keys]
        print(f"Vantage API keys for account [{ACCOUNT_ID}]:\n")

    elif task == "external_keys":
        keys = vantage_instance.get_external_api_keys()
        res = [key.actual_instance.dict() for key in keys]
        print(f"External API keys for account [{ACCOUNT_ID}]:\n")

    elif task == "list_collections":
        collections = vantage_instance.list_collections()
        res = [col.actual_instance.dict() for col in collections]
        print(f"Collections created for account [{ACCOUNT_ID}]:\n")

    elif task == "create_collection":
        collection = vantage_instance.create_collection(
            collection_id=collection_id,
            collection_name=DEFAULT_COLLECTION_NAME,
            user_provided_embeddings=USER_PROVIDED_EMBEDDINGS,
            embeddings_dimension=DEFAULT_LLM_EMBEDDINGS_DIM,
            llm=DEFAULT_LLM,
            external_key_id=EXTERNAL_KEY_ID,
        )
        res = collection.dict()
        print(
            f"Created collection with id: {collection.collection_id}. Details:\n"
        )

    elif task == "update_collection":
        collection = vantage_instance.update_collection(
            collection_id=collection_id,
            collection_name=DEFAULT_UPDATE_COLLECTION_NAME,
        )
        res = collection.dict()
        print(
            f"Updated collection with id: {collection.collection_id}. Details:\n"
        )

    elif task == "get_collection":
        collection = vantage_instance.get_collection(
            collection_id,
        )
        res = collection.dict()
        print(f"Collection with id: {collection.collection_id}. Details:\n")

    elif task == "browser_url":
        upload_url = vantage_instance.get_browser_upload_url(
            collection_id=collection_id,
            file_size=3000,
        )
        res = upload_url.dict()
        print(
            f"Upload browser URL for collection with id: {collection_id}. Details:\n"
        )

    elif task == "upload_file":
        res = vantage_instance.upload_embedding_by_path(
            collection_id=collection_id, file_path=file_path
        )
        print("Uploading file returned status:")

    elif task == "delete_collection":
        collection = vantage_instance.delete_collection(
            collection_id,
        )
        res = collection.dict()
        print(
            f"Deleted collection with id: {collection.collection_id}. Details:\n"
        )

    elif task == "semantic_search":
        result = vantage_instance.semantic_search(
            text=query_text,
            collection_id=collection_id,
            vantage_api_key=VANTAGE_API_KEY,
        )
        res = result.dict()
        print("Semantic search results:\n")

    pprint(res)


if __name__ == "__main__":
    parser = ArgumentParser()

    tasks = [
        "vantage_keys",
        "external_keys",
        "list_collections",
        "create_collection",
        "update_collection",
        "get_collection",
        "delete_collection",
        "semantic_search",
        "browser_url",
        "delete_collection",
        "upload_file",
    ]

    parser.add_argument(
        "-t",
        "--task",
        default=DEFAULT_TASK,
        choices=tasks,
    )
    parser.add_argument(
        "-f",
        "--file_path",
        type=str,
    )
    parser.add_argument(
        "-cid",
        "--collection_id",
        default=DEFAULT_COLLECTION_ID,
        type=str,
    )
    parser.add_argument(
        "-qt",
        "--query_text",
        default=DEFAULT_QUERY_TEXT,
        type=str,
    )
    args = parser.parse_args()

    main(args.task, args.collection_id, args.file_path, args.query_text)
