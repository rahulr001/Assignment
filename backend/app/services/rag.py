from loguru import logger  # Use Loguru for logging
from app.dependencies import chroma_client, openai_client


# Function to generate embedding for a given text using OpenAI API
def generate_embedding(text: str) -> list:
    """
    Generate an embedding vector for the provided text using OpenAI's API.

    Args:
        text (str): The input text to generate embedding for.

    Returns:
        list: The embedding vector as a list of floats.

    Raises:
        Exception: If the embedding generation fails.
    """
    try:
        logger.debug("Generating embedding for text: '{}'", text)
        # Call OpenAI API to generate embedding
        response = openai_client.embeddings.create(
            input=text, model="text-embedding-ada-002"
        )
        logger.info("Embedding generated successfully.")
        return response.data[0].embedding
    except Exception as e:
        logger.error("Failed to generate embedding: {}", str(e), exc_info=True)
        raise


def add_document(collection, text: str, metadata: dict):
    """
    Adds a document to the specified collection with its embedding and metadata.

    Args:
        collection: The ChromaDB collection object.
        text (str): The document text to embed and store.
        metadata (dict): Metadata associated with the document (must include 'id').
    """
    try:
        logger.debug("Generating embedding for new document.")
        embedding = generate_embedding(text)
        logger.debug(f"Adding document with ID: {metadata.get('id')} to collection.")
        collection.add(
            embeddings=[embedding],
            metadatas=[metadata],
            documents=[text],
            ids=[metadata["id"]],
        )
        logger.info(f"Added document with ID: {metadata['id']}")
    except Exception:
        logger.exception(f"Failed to add document with ID: {metadata.get('id')}")
        raise


def query_collection(collection: str, query_text: str, n_results: int = 5):
    """
    Queries the specified collection for documents similar to the query text.

    Args:
        collection (str): The name of the collection to query.
        query_text (str): The text to query against the collection.
        n_results (int): Number of top results to retrieve.

    Returns:
        dict: Query results from the collection.
    """
    try:
        logger.debug(f"Retrieving '{collection}' collection from Chroma client.")
        collection_instance = chroma_client.get_collection(name=collection)
        logger.debug("Generating embedding for query text.")
        query_embedding = generate_embedding(query_text)
        logger.debug(f"Querying collection for top {n_results} results.")
        results = collection_instance.query(
            query_embeddings=[query_embedding], n_results=n_results
        )
        logger.info(
            f"Retrieved {len(results['documents'][0])} documents for query: '{query_text}'"
        )
        return results
    except Exception:
        logger.exception(f"Failed to query collection for text: '{query_text}'")
        raise
