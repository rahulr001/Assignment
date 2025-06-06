from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import search
from loguru import logger
from scripts.ingest_data import ingest_apparels_data
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.
    Initializes cache and ingests apparel data at startup.
    Cleans up resources at shutdown.
    """
    logger.info("Initializing application lifespan.")
    # Ingest apparel data at startup
    try:
        ingest_apparels_data()
        logger.success("Apparel data ingested successfully.")
    except Exception as e:
        logger.error(f"Error during apparel data ingestion: {e}")

    yield  # Application runs here

    logger.info("Application shutdown completed.")


# Create FastAPI app with lifespan handler
app = FastAPI(
    title="Conversational Search API",
    description="A backend for conversational search and recommendations using ChromaDB and OpenAI.",
    version="1.0.0",
    lifespan=lifespan,
)


# Configure CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change this for production security)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include API routers
app.include_router(search.router)
