<img src="assets/vantage_logo.png" title="Vantage Discovery Logo" width="300"/></br>

# Vantage Discovery Python SDK

The Vantage Discovery Python SDK provides an easy-to-use interface to interact with the Vantage vector database, enabling developers to seamlessly integrate vector search and collection management capabilities into their Python applications.

## Installation

To install the Vantage Python SDK, run the following command:

```bash
pip install vantage-sdk
```

## Quickstart

To get started with the Vantage Python SDK, you'll need to set up your Vantage account and obtain your API keys. Once you have your credentials, you can initialize the VantageClient to begin managing collections and performing searches.

```python
from vantage_sdk import VantageClient

# Initialize the VantageClient with your Vantage API key and Account ID
vantage_client = VantageClient.using_vantage_api_key(
    vantage_api_key='YOUR_VANTAGE_API_KEY',
    account_id='YOUR_ACCOUNT_ID'
)

# Now you can use the client to manage collections, documents, and perform searches
```

## Overview

The Vantage Discovery Python SDK is divided into several modules, allowing you to manage accounts, collections, and API keys, as well as perform various types of searches.

#### Key Features
- __Collection Management__: Easily create, update, list, and delete collections.
- __Documents Upload__: Upload your data easily to your collections.
- __Search__: Perform semantic, embedding and "more like this/these" searches within your collections.
- __LLM Keys Management__: Keep your LLM provider secrets safe and up-to-date.

## Examples

### Creating a Collection

```python
collection = vantage_client.create_collection(
    collection_id="my_collection",
    collection_name="My Test Collection",
    embeddings_dimension=1536,
    llm="text-embedding-ada-002",
    external_key_id="YOUR_EXTERNAL_KEY_ID" # Get from Vantage Console UI or using the SDK
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

### Performing a Search
```python
search_result = vantage_client.semantic_search(
    text="Find documents similar to this text",
    collection_id="my_collection"
)
for result in search_result.results:
    print(result.id, result.score)
```

## Documentation

For detailed documentation on all methods and their parameters, please refer to the [Vantage Discovery Python SDK repository](https://github.com/VantageDiscovery/vantage-sdk-python) or check some of the examples from our [Vantage Tutorials repository](https://github.com/VantageDiscovery/vantage-tutorials).
