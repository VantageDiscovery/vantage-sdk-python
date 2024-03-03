# [Vantage Discovery Pyton SDK](https://github.com/VantageDiscovery/vantage-sdk-python)

The Vantage Discovery Python SDK provides an easy-to-use interface to interact with the Vantage vector database, enabling developers to seamlessly integrate vector search and collection management capabilities into their Python applications.

## Installation

To install the Vantage Python SDK, run the following command:

```bash
pip install vantage-sdk
```

## Quickstart

To get started with the Vantage Python SDK, you'll need to set up your Vantage account and obtain your API keys. Once you have your credentials, you can initialize the VantageClient to begin managing collections and performing searches.

```python
from vantage import VantageClient

# Initialize the VantageClient with your account details
vantage_client = VantageClient.using_client_credentials(
    vantage_client_id='YOUR_CLIENT_ID',
    vantage_client_secret='YOUR_CLIENT_SECRET',
    account_id='YOUR_ACCOUNT_ID'
)

# Now you can use the client to manage collections, documents, and perform searches
```

## Overview

The Vantage Discovery Python SDK is divided into several modules, allowing you to manage accounts, collections, and API keys, as well as perform various types of searches.

#### Key Features
- Collection Management: Easily create, update, list, and delete collections.
- Documents Upload: Upload your data easily to your collections.
- Search: Perform semantic, embedding and "more like this" searches within your collections.
- LLM Keys Management: Keep your LLM provider secrets safe and up-to-date.

## Examples

### Creating a Collection

```python
collection = vantage_client.create_collection(
    collection_id="my_collection",
    collection_name="My Test Collection",
    embeddings_dimension=128
)
print(f"Created collection: {collection.name}")
```

### Uploading Documents
```python
documents_jsonl = '{"id": "1", "text": "Example text"}\\n{"id": "2", "text": "Another example"}'
vantage_client.upload_documents_from_jsonl(
    collection_id="my_collection",
    documents=documents_jsonl
)
```

## Performing a Search

```python
search_result = vantage_client.semantic_search(
    text="Find documents similar to this text",
    collection_id="my_collection"
)
for result in search_result.results:
    print(result.document_id, result.score)
```

## Documentation 

For detailed documentation on all methods and their parameters, please refer to the official [Vantage Discovery Python SDK repositry](https://github.com/VantageDiscovery/vantage-sdk-python) or check some of the examples from our [Vantage Tutorials repository](https://github.com/VantageDiscovery/vantage-tutorials).