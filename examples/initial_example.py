"""
[WIP]
Initial example of the Vantage Python SDK Usage. 
Please set your ACCOUNT_ID and environment variables accordingly.
"""

from argparse import ArgumentParser
import os
from pprint import pprint

from vantage import Vantage


ACCOUNT_ID = "<YOUR_ACCOUNT_ID>"
COLLECTION_ID = "test-sdk"
COLLECTION_NAME = "Test SDK"
NEW_COLLECTION_NAME = "New Test SDK Name"  # Used in update_collection method


def main(task: str, collection_id: str) -> None:
    vantage_instance = Vantage.from_defaults(
        vantage_client_id=os.environ["VANTAGE_API_CLIENT_ID"],
        vantage_client_secret=os.environ["VANTAGE_API_CLIENT_SECRET"],
    )

    if task == "user":
        user = vantage_instance.logged_in_user()
        res = user.to_dict()

    elif task == "list":
        collections = vantage_instance.list_collections(ACCOUNT_ID)
        res = [col.to_dict() for col in collections]
        print(f"Collections created for account [{ACCOUNT_ID}]:\n")

    elif task == "create":
        collection = vantage_instance.create_collection(
            account_id=ACCOUNT_ID,
            collection_id=collection_id,
            collection_name=COLLECTION_NAME,
            user_provided_embeddings=True,
            embeddings_dimension=1536,
        )
        res = collection.to_dict()
        print(
            f"Created collection with id: {collection.collection_id}. Details:\n"
        )

    elif task == "update":
        collection = vantage_instance.update_collection(
            collection_id=collection_id,
            account_id=ACCOUNT_ID,
            collection_name=NEW_COLLECTION_NAME,
        )
        res = collection.to_dict()
        print(
            f"Updated collection with id: {collection.collection_id}. Details:\n"
        )

    elif task == "get":
        collection = vantage_instance.get_collection(
            collection_id,
            ACCOUNT_ID,
        )
        res = collection.to_dict()
        print(f"Collection with id: {collection.collection_id}. Details:\n")

    elif task == "delete":
        collection = vantage_instance.delete_collection(
            collection_id,
            ACCOUNT_ID,
        )
        res = collection.to_dict()
        print(
            f"Deleted collection with id: {collection.collection_id}. Details:\n"
        )

    pprint(res)


if __name__ == "__main__":
    parser = ArgumentParser()

    tasks = ["user", "list", "create", "update", "get", "delete"]

    parser.add_argument("-t", "--task", default="user", choices=tasks)
    parser.add_argument(
        "-cid", "--collection_id", default=COLLECTION_ID, type=str
    )
    args = parser.parse_args()

    main(args.task, args.collection_id)
