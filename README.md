<img src="assets/vantage_logo.png" title="Vantage Discovery Logo" width="300"/></br>

# Vantage Discovery Python SDK

The Vantage Discovery Python SDK provides an easy-to-use interface to interact with the Vantage vector database, enabling developers to seamlessly integrate vector search and collection management capabilities into their Python applications.

## Installation

To install the [Vantage Python SDK](https://pypi.org/project/vantage-sdk/), run the following command:

```bash
pip install vantage-sdk
```

## Quickstart

To get started with the Vantage Python SDK, you'll need to set up your [Vantage account](https://console.vanta.ge/) and obtain your account ID and Vantage API key. Once you have your ID and key, you can initialize the VantageClient which you can then use to manage your account, collections and keys and perform searches.

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

The Vantage Discovery Python SDK is divided into several modules, allowing you to manage account, collections, and API keys, as well as perform various types of searches.

#### Key Features
- __Collection Management__: Easily create, update, list, and delete collections.
- __Documents Upload__: Upload your data easily to your collections.
- __Search__: Perform semantic, embedding and "more like this/these" searches within your collections.
- __LLM Keys Management__: Keep your LLM provider secrets safe and up-to-date.

## 🔍 Examples

### Creating a Collection

To create a new collection for storing documents, specify the collection ID, the dimension of the embeddings, and the LLM (language learning model) details. Here, we use `text-embedding-ada-002` from OpenAI with the necessary secret key.

📚 Visit [management-api](https://docs.vantagediscovery.com/docs/management-api) documentation for more details.

```python
collection = OpenAICollection(
    collection_id="my-collection",
    embeddings_dimension=1536,
    llm="text-embedding-ada-002",
    llm_secret="YOUR_OPENAI_SECRET_KEY",
)

created_collection = vantage_client.create_collection(collection=collection)

print(f"Created collection: {created_collection.collection_name}")
```

### Uploading Documents

To upload documents to your collection, provide a list of document IDs and corresponding text. Each document is wrapped in a `VantageManagedEmbeddingsDocument` object. This example demonstrates uploading a batch of documents.

📚 Visit [management-api](https://docs.vantagediscovery.com/docs/management-api) documentation for more details.

```python
ids = [
    "1",
    "2",
    "3",
    "4",
]

texts = [
    "First text",
    "Second text",
    "Third text",
    "Fourth text",
]

documents = [
    VantageManagedEmbeddingsDocument(text=text, id=id)
    for id, text in zip(ids, texts)
]

instance.upsert_documents(
    collection_id="my-collection",
    documents=documents,
)
```

### Performing a Search

To perform a semantic search within your collection, specify the text you want to find similar documents for. This example retrieves documents similar to the provided text, printing out each document's ID and its similarity score.

📚 Visit [search-api](https://docs.vantagediscovery.com/docs/search-api) documentation for more details.

```python
search_result = vantage_client.semantic_search(
    text="Find documents similar to this text",
    collection_id="my-collection"
)
for result in search_result.results:
    print(result.id, result.score)
```

## 📚 Documentation

For detailed documentation on all methods and their parameters, please refer to the [Vantage Discovery official documentation](https://docs.vantagediscovery.com/docs/concepts).
