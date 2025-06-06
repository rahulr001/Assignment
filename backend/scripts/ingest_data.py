import pandas as pd
from app.dependencies import chroma_client
from app.services.rag import add_document
from loguru import logger


def ingest_apparels_data():
    """
    Ingest Apparels product data and reviews into a ChromaDB collection.
    """
    try:
        # Load Excel data from uploaded file path
        df = pd.read_excel("data/Apparels_shared.xlsx")
        logger.info(f"Loaded {len(df)} records from Apparels_shared.xlsx")

        # Try to get existing ChromaDB collection
        try:
            collection = chroma_client.get_collection("Apparels")
            logger.info("Using existing 'Apparels' collection, skipping ingestion")
            return  # Exit if collection already exists
        except Exception:
            collection = chroma_client.create_collection("Apparels")
            logger.info("Created new 'Apparels' collection")

        # Ingest each row from the DataFrame
        for index, row in df.iterrows():
            # Build metadata
            metadata = {
                "id": str(row.get("id")),
                "name": row.get("name"),
                "category": row.get("category"),
                "available_sizes": row.get("available_sizes"),
                "fit": row.get("fit"),
                "fabric": row.get("fabric"),
                "sleeve_length": row.get("sleeve_length"),
                "color_or_print": row.get("color_or_print"),
                "occasion": row.get("occasion"),
                "neckline": row.get("neckline"),
                "length": row.get("length"),
                "pant_type": row.get("pant_type"),
                "price": float(row.get("price", 0)),
            }

            # Create a descriptive text for embedding
            text_parts = [
                f"{key.replace('_', ' ').title()}: {value}"
                for key, value in metadata.items()
                if pd.notnull(value)
            ]
            text_parts.insert(0, f"Product Name: {row.get('name', '')}")
            text = " | ".join(text_parts)

            # Add document to the collection
            add_document(collection, text, metadata)
            logger.debug(f"Ingested product: {row.get('name')} (ID: {row.get('id')})")

        logger.success("Data ingestion completed successfully")
    except Exception as e:
        logger.error(f"Data ingestion failed: {str(e)}", exc_info=True)
        raise
