# AI Code Review Bot - Backend

A FastAPI-based backend for an AI-powered code review assistant. It combines static analysis (AST/regex) with LLM-based analysis (Hugging Face) to provide comprehensive code feedback and **auto-fixing** capabilities.

## Features

- **Hybrid Analysis**: Combines Python's `ast` / regex checks with GPT-4.
- **Auto-Fix**: Automatically refactors and fixes code based on best practices.
- **Support**: Python, JavaScript, Java, C++.
- **Endpoints**:
  - `POST /api/review`: Submit code for review.
  - `POST /api/auto-fix`: Submit code for automated fixing.
  - `GET /health`: Check service status.

## Dependencies

- Python 3.10+
- FastAPI
- Pydantic
- Hugging Face Hub

## Setup

1. **Install Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Environment Variables**
   Create a `.env` file in the `backend/` directory:
   ```env
   HUGGINGFACE_API_TOKEN=hf_...
   # Optional
   LLM_MODEL=meta-llama/Meta-Llama-3-8B-Instruct
   ```

3. **Run the Server**
   ```bash
   uvicorn app.main:app --reload
   ```
   The API will be available at `http://localhost:8000`.

## API Usage

### 1. Review Code

**Request:**
```bash
curl -X POST "http://localhost:8000/api/review" \
     -H "Content-Type: application/json" \
     -d '{
           "language": "python",
           "code": "def foo():\n    print(\"hello\")"
         }'
```

### 2. Auto-Fix Code (NEW)

**Request:**
```bash
curl -X POST "http://localhost:8000/api/auto-fix" \
     -H "Content-Type: application/json" \
     -d '{
           "language": "python",
           "code": "def add(a,b):return a+b"
         }'
```

**Response:**
```json
{
  "fixed_code": "def add(a: int, b: int) -> int:\n    \"\"\"\n    Adds two numbers and returns the result.\n    \"\"\"\n    return a + b",
  "summary": "Added type hints and a docstring to improve readability and type safety.",
  "changes": [
    {
      "line": 1,
      "before": "def add(a,b):return a+b",
      "after": "def add(a: int, b: int) -> int: ...",
      "reason": "Added type hints and formatted code."
    }
  ]
}
```

## Safety & Constraints

- **Max Code Length**: Validated to prevent large payload attacks.
- **LLM Output**: Strictly enforced JSON structure.
- **Safe Refactoring**: The model is instructed to preserve logic and avoid adding new features.
