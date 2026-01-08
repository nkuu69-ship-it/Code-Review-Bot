# AI Code Review Bot

An AI-powered code review assistant that combines static analysis with LLM capabilities to provide comprehensive code feedback and automated fixes. Contains a FastAPI backend and a Next.js frontend.

## Features

- **Hybrid Analysis**: Combines Python's `ast` / regex checks with LLMs (Llama 3 / Zephyr).
- **Auto-Fix**: Automatically refactors and fixes code based on best practices.
- **Modern UI**: Clean, responsive interface built with Next.js and Tailwind CSS.
- **Multi-Language Support**: Python, JavaScript, Java, C++.

## Project Structure

- `backend/`: FastAPI server handling analysis and LLM interactions.
- `frontend/`: Next.js web application for user interaction.

## Tech Stack

- **Backend**: Python 3.10+, FastAPI, Pydantic, Hugging Face Inference API.
- **Frontend**: Next.js 16, React 19, TypeScript, Tailwind CSS, Shadcn UI.

## Getting Started

### Prerequisites

- Node.js 18+ and npm/pnpm.
- Python 3.10+ and pip.
- Hugging Face API Token (for LLM features).

### Installation & Setup

#### 1. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure Environment
# Create a .env file in backend/ directory
echo "HUGGINGFACE_API_TOKEN=your_token_here" > .env
```

#### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
# or
pnpm install
```

### Running the Application

**Start the Backend:**
```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload
```
The API will run at `http://localhost:8000`.

**Start the Frontend:**
```bash
cd frontend
npm run dev
```
The web app will run at `http://localhost:3000`.

## API Usage

- **Determine Issues**: `POST /api/review`
- **Auto-Fix Code**: `POST /api/auto-fix`

Example `curl` for Auto-Fix:
```bash
curl -X POST "http://localhost:8000/api/auto-fix" \
     -H "Content-Type: application/json" \
     -d '{
           "language": "python",
           "code": "def add(a,b):return a-b"
         }'
```

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push to the branch.
5. Create a Pull Request.
