# Live Demo URLs

You can test the live deployments here:

- **Backend API Docs:** [https://conv-assessment-api.rokkun.io/docs](https://conv-assessment-api.rokkun.io/docs)
- **Frontend App:** [https://conv-assessment.rokkun.io/](https://conv-assessment.rokkun.io/)

---

# Prerequisites

Before setting up the project, ensure you have the following installed:

- **Backend**: Python 3.11
- **Frontend**: Node.js 22.x and npm (or yarn)

---

# Conversational Search Backend

A production-ready FastAPI backend for a conversational search and recommendation system using ChromaDB and OpenAI. This backend is designed for personalized product recommendations through a conversational interface.

---

## Features

- **Conversational Search API**: Handles multi-turn conversations and follow-up questions.
- **Personalized Recommendations**: Uses user input to generate optimized product queries and recommendations.
- **ChromaDB Integration**: Stores and retrieves product data with vector search.
- **OpenAI Integration**: Leverages OpenAI models for conversation and embedding generation.
- **Session Management**: In-memory session cache for multi-turn conversations.
- **Robust Logging**: Uses Loguru for detailed logging.

---

## Project Structure

```
project/
├── backend/
│   ├── requirements.txt                # Python dependencies
│   ├── app/
│   │   ├── __init__.py
│   │   ├── dependencies.py             # OpenAI and ChromaDB client setup
│   │   ├── main.py                     # FastAPI app entry point
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   └── search.py               # API endpoints
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── embedding.py            # Embedding generation logic
│   │   │   └── rag.py                  # Retrieval-augmented generation logic
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── constants.py            # Project-wide constants
│   │   │   └── pipeline.py             # Conversation pipeline
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── schemas.py              # Pydantic models for requests and state
│   │   └── ...                         # __pycache__ and other files
│   ├── chroma_db/                      # ChromaDB persistent storage
│   │   └── ...
│   ├── data/
│   │   └── skincare_catalogue.xlsx     # Product data (Excel)
│   ├── scripts/
│   │   ├── __init__.py
│   │   └── ingest_data.py              # Data ingestion script
│   │   └── ...                         # __pycache__
├── frontend/
│   ├── eslint.config.js                # ESLint configuration
│   ├── index.html                      # HTML entry point
│   ├── package.json                    # Frontend dependencies
│   ├── vite.config.js                  # Vite configuration
│   └── src/                            # Source files
│       ├── App.css                     # App-level CSS
│       ├── App.jsx                     # Main App component
│       ├── index.css                   # Global CSS
│       ├── main.jsx                    # Entry point for React
│       └── search.jsx                  # Search component
├── setup.sh                            # Setup script
└── README.md                           # Project documentation
```

---

## Setup

### 1. Clone the Repository

```bash
git clone https://projects.rokkun.io/rahul_techactive/conversational-store-assessment.git
cd conversational-store-assessment
```

---

### 2. Quick Setup (Recommended)

Run the provided setup script to set up both backend and frontend in one step:

```bash
bash setup.sh
```

This script will:

- Create a Python virtual environment and install backend dependencies
- Set up the frontend application (if present)
- Prompt for environment variables

---

### 3. Manual Setup

#### Backend

1. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Environment Variables**

   Create a `.env` file in the project root and add your OpenAI API key:

   ```
   OPENAI_API_KEY=your-openai-api-key
   ```

   Or export it in your shell:

   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   ```

#### Frontend (Vite React)

If you have a frontend application (e.g., in `frontend/`):

1. **Navigate to the frontend directory**

   ```bash
   cd frontend
   ```

2. **Install frontend dependencies**

   ```bash
   npm install
   # or
   yarn
   ```

3. **Start the frontend development server**

   ```bash
   npm run dev
   # or
   yarn dev
   ```

   The frontend (Vite) will typically run on [http://localhost:5173](http://localhost:5173).

---

## Running the Application

### Backend

- **Development**

  ```bash
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
  ```

- **Production (with Gunicorn)**

  ```bash
  gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
  ```

### Frontend

- See the [Frontend (Vite React)](#frontend-vite-react) section above for development instructions.

---

## API Endpoints

### `POST /api/search`

- **Request Body**:
  ```json
  {
    "query": "string",
    "session_id": "string (optional)"
  }
  ```
- **Response**:
  ```json
  {
    "conversation": [
      {
        "role": "string",
        "content": "string"
      }
    ],
    "query": "string",
    "follow_up_question": "string",
    "recommendation": "string",
    "recommendation_query": "string",
    "citations": ["string"],
    "ready_for_recommendation": "boolean"
  }
  ```
