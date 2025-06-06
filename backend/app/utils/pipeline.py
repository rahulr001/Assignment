from app.models.schemas import ConversationState, ResponseFormat
from app.services.rag import query_collection
from langgraph.graph import StateGraph, END, START
from app.dependencies import openai_client
from loguru import logger
from app.utils.constants import (
    ANALYZE_ANSWERS_PROMPT,
    FOLLOW_UP_QUESTION_PROMPT,
    RECOMMENDATION_PROMPT_TEMPLATE,
)

# ----------- Pipeline Node Functions -----------


def ask_follow_up_questions(state):
    """
    Asks a direct follow-up question based on the current conversation state.
    """
    logger.info("Entering ask_follow_up_questions with state: {}", state)
    if state.ready_for_recommendation:
        logger.info(
            "State is ready for recommendation, skipping follow-up questions.")
        return state
    system_prompt = FOLLOW_UP_QUESTION_PROMPT
    messages = [
        {"role": "system", "content": system_prompt},
        *state.conversation,
    ]
    follow_up = ask_ai(messages)
    logger.debug("Generated follow-up question: {}", follow_up)
    state.follow_up_question = follow_up

    return state


def analyze_answers(state):
    """
    Analyzes user answers to determine if enough information is present for recommendations.
    """
    logger.info("Analyzing answers in state: {}", state)
    full_conversation = "\n".join(
        [f"{msg['role']}: {msg['content']}" for msg in state.conversation]
    )
    system_prompt = ANALYZE_ANSWERS_PROMPT
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user",
            "content": f"conversation: \n {full_conversation}"},
    ]
    response = ask_ai_json(messages)
    logger.debug("AI analyze_answers raw response: {}", response)
    state.ready_for_recommendation = response.ready_for_recommendation
    state.recommendation_query = response.optimized_query
    logger.info(
        "Analysis result - ready_for_recommendation: {}, optimized_query: {}",
        state.ready_for_recommendation,
        state.recommendation_query,
    )
    return state


def recommend_products(state):
    """
    Queries the product collection and generates recommendations based on the optimized query.
    """
    logger.info(
        "Recommending products for query: {}",
        getattr(state, "recommendation_query", None),
    )
    results = query_collection("Apparels", state.recommendation_query)
    # Rank products by margin
    doc_metadata_pairs = list(
        zip(
            results["documents"][0],
            results["metadatas"][0],
        )
    )
    top_docs, top_metadata = (
        zip(*doc_metadata_pairs[:5]) if doc_metadata_pairs else ([], [])
    )
    state.citations = top_metadata
    recommendation_prompt = RECOMMENDATION_PROMPT_TEMPLATE.format(
        product_data=top_metadata
    )
    messages = [
        {"role": "system", "content": recommendation_prompt},
        {"role": "user", "content": state.recommendation_query},
    ]
    logger.debug("Sending recommendation prompt to AI: {}",
                 recommendation_prompt)
    state.recommendation = ask_ai(messages)
    logger.info("Generated recommendation: {}", state.recommendation)
    return state


# ----------- Helper Functions -----------


def ask_ai(messages):
    """
    Sends messages to the OpenAI client and returns the response.
    """
    logger.debug("Sending messages to OpenAI: {}", messages)
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=500,
        temperature=0.7,
    )
    content = response.choices[0].message.content.strip()
    logger.debug("Received response from OpenAI: {}", content)
    return content


def ask_ai_json(messages):
    """
    Sends messages to the OpenAI client and returns the response.
    """
    logger.debug("Sending messages to OpenAI: {}", messages)
    response = openai_client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=100,
        temperature=0.7,
        response_format=ResponseFormat,
    )
    content = response.choices[0].message.parsed
    logger.debug("Received response from OpenAI: {}", content)
    return content


def build_graph():
    """
    Builds and compiles the conversation pipeline graph.
    """
    logger.info("Building the StateGraph pipeline.")
    graph = StateGraph(state_schema=ConversationState)

    graph.add_node("ask_questions", ask_follow_up_questions)
    graph.add_node("analyze_answers", analyze_answers)
    graph.add_node("recommend_products", recommend_products)

    # graph.set_entry_point("ask_questions")

    graph.add_edge(START, "analyze_answers")

    graph.add_conditional_edges(
        "analyze_answers",
        lambda state: state.ready_for_recommendation,
        {True: "recommend_products", False: "ask_questions"},
    )
    graph.add_edge("ask_questions", END)
    graph.add_edge("recommend_products", END)

    logger.info("StateGraph pipeline compiled successfully.")
    return graph.compile()
