import { useState, useRef, useEffect } from "react";
import Markdown from "react-markdown";
import CitationsTable from "./CitationsTable";

const Search = () => {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [chatMessages, setChatMessages] = useState([]);
  const [sessionId, setSessionId] = useState("");
  const [readyForRecommendation, setReadyForRecommendation] = useState(false);
  const [citations, setCitations] = useState([]);

  const messagesStartRef = useRef(null);

  // Function to generate new session ID
  const generateNewSessionId = () => {
    return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(
      /[xy]/g,
      function (c) {
        const r = (Math.random() * 16) | 0,
          v = c === "x" ? r : (r & 0x3) | 0x8;
        return v.toString(16);
      }
    );
  };

  // Generate UUID for session on initial load
  useEffect(() => {
    setSessionId(generateNewSessionId());
  }, []);

  // Auto scroll to the newest message at the top when messages change
  useEffect(() => {
    if (messagesStartRef.current && chatMessages.length > 0) {
      messagesStartRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [chatMessages]);

  const handleInputChange = (e) => {
    setQuery(e.target.value);
  };

  const handleClear = () => {
    setQuery("");
  };

  // Handle refresh/reset chat
  const handleRefresh = () => {
    setChatMessages([]);
    setError(null);
    setQuery("");
    setSessionId(generateNewSessionId());
    setReadyForRecommendation(false);
    setCitations([]);
  };

  const handleSearch = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setError(null);

    // Create user message
    const userMessage = {
      role: "user",
      content: query,
    };

    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/api/search`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            query: query,
            session_id: sessionId,
          }),
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();

      // Update ready for recommendation state
      setReadyForRecommendation(data.ready_for_recommendation);

      // Store citations separately
      setCitations(data.citations || []);

      // Set new messages array with only the latest exchange
      if (data.ready_for_recommendation) {
        // Case 1: Ready for recommendation - show recommendation text or default message
        const recommendationContent = data.recommendation || "Here are the recommended items based on your preferences:";
        setChatMessages([
          {
            role: "assistant",
            content: recommendationContent,
            type: "recommendation",
          },
          userMessage,
        ]);
      } else if (data.follow_up_question) {
        // Case 2: Follow-up question
        setChatMessages([
          {
            role: "assistant",
            content: data.follow_up_question,
            type: "follow_up",
          },
          userMessage,
        ]);
      }

      // Clear search input
      setQuery("");
    } catch (err) {
      console.error("Search error:", err);
      setError("An error occurred while searching. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  return (
    <div className="flex flex-col h-screen bg-white">
      {/* Header with search input area */}
      <div className="p-8 border-b border-gray-100 sticky top-0 z-10 bg-white">
        <div className="flex items-center justify-between mb-3">
          <h1 className="text-lg font-medium text-gray-800">
            Search Assistant
          </h1>
          <button
            className="text-gray-400 hover:text-gray-600 transition-colors"
            onClick={handleRefresh}
            title="Start new chat"
          >
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
              />
            </svg>
          </button>
        </div>
        <div className="flex items-center gap-2">
          <div className="relative flex-grow">
            <div className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">
              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                />
              </svg>
            </div>
            <input
              type="text"
              className="w-full p-2.5 pl-10 pr-10 border border-gray-200 rounded-full focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
              placeholder="Type your question..."
              value={query}
              onChange={handleInputChange}
              onKeyDown={handleKeyDown}
            />
            {query.length > 0 && (
              <button
                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-500"
                onClick={handleClear}
              >
                <svg
                  className="w-4 h-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            )}
          </div>
          <button
            className={`p-2.5 rounded-full bg-blue-500 hover:bg-blue-600 text-white transition-colors ${
              loading ? "opacity-70 cursor-not-allowed" : ""
            }`}
            onClick={handleSearch}
            disabled={loading}
          >
            {loading ? (
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
            ) : (
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M9 5l7 7-7 7"
                />
              </svg>
            )}
          </button>
        </div>
      </div>

      {/* Error message */}
      {error && (
        <div className="mx-8 mt-4">
          <div className="bg-red-50 text-red-600 p-3 rounded-lg text-sm border border-red-100">
            {error}
          </div>
        </div>
      )}

      {/* Chat area - Takes up the rest of the screen */}
      <div className="flex-grow overflow-y-auto p-4">
        <div ref={messagesStartRef} />

        <div className="mx-6 rounded-lg">
          {/* Show only the assistant message (the first one in the array) */}
          {chatMessages[0] && (chatMessages[0].role === "assistant") && (
            <div className="p-4 bg-gray-50 border border-gray-100 rounded-lg">
              <Markdown>{chatMessages[0].content}</Markdown>

              {/* Show citations table when ready for recommendation and citations exist */}
              {readyForRecommendation && citations && citations.length > 0 && (
                <CitationsTable citations={citations} />
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Search;
