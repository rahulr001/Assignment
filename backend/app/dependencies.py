import os
from openai import OpenAI
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
import openai
from loguru import logger

# -----------------------------------------------------------
# Load environment variables from .env file
# -----------------------------------------------------------
try:
    load_dotenv()
    logger.info("Environment variables loaded from .env file.")
except Exception as e:
    logger.error(f"Failed to load environment variables: {e}")

# -----------------------------------------------------------
# Initialize OpenAI API key from environment variables
# -----------------------------------------------------------
openai.api_key = os.getenv("OPENAI_API_KEY")
if openai.api_key:
    logger.info("OpenAI API key loaded successfully.")
else:
    logger.warning("OpenAI API key not found in environment variables.")

# -----------------------------------------------------------
# Initialize OpenAI client
# -----------------------------------------------------------
try:
    openai_client = OpenAI()
    logger.info("OpenAI client initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize OpenAI client: {e}")

# -----------------------------------------------------------
# Initialize ChromaDB client with persistent storage
# -----------------------------------------------------------
try:
    chroma_client = chromadb.PersistentClient(
        path="./chroma_db", settings=Settings(anonymized_telemetry=False)
    )
    logger.info("ChromaDB PersistentClient initialized at './chroma_db'.")
except Exception as e:
    logger.error(f"Failed to initialize ChromaDB PersistentClient: {e}")
