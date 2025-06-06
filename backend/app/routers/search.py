from typing import Dict
import uuid
from fastapi import APIRouter, HTTPException, Request
from app.models.schemas import SearchRequest
from loguru import logger
from app.utils.pipeline import ConversationState, build_graph

router = APIRouter(prefix="/api", tags=["search"])

conversation_sessions: Dict[str, ConversationState] = {}

# with open("/home/saber/Downloads/vibe-product-recomentor/src/backend/prompt.txt", "r") as file:
#     system_prompt = file.read()


@router.post("/search")
async def search(request: Request, data: SearchRequest):
    """
    Handles search requests, manages session cache, and invokes the product pipeline.
    """
    try:
        # Generate or retrieve session ID
        session_id = data.session_id or str(uuid.uuid4())
        _cache = conversation_sessions

        # Initialize cache for new sessions
        if session_id not in _cache:
            logger.debug(
                f"Initializing new session cache for session_id: {session_id}")
            _cache[session_id] = ConversationState(
                conversation=[], query=data.query)

        cache = _cache[session_id].conversation
        # Append user query to conversation cache
        cache.append({"role": "user", "content": data.query})
        # response = ask_ai(
        #     [{"role": "system", "content": system_prompt}] + cache
        # )
        # return response
        logger.info(
            f"Received search query: {data.query} | session_id: {session_id}")

        # Build and invoke the product pipeline
        product_pipeline = build_graph()
        logger.debug(
            "Invoking product pipeline with current conversation state.")
        result = product_pipeline.invoke(
            ConversationState(
                conversation=cache, query=data.query, ready_for_recommendation=False
            )
        )

        # Append assistant's follow-up question to cache
        follow_up = result.get("follow_up_question")
        if follow_up:
            cache.append({"role": "assistant", "content": follow_up})
            logger.debug(f"Appended assistant response to cache: {follow_up}")

        logger.debug(f"Current conversation cache: {cache}")

        logger.success("Search query processed successfully.")
        return result
    except Exception as e:
        logger.error(f"Error processing search query: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
