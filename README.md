# AI-Powered API Automation Framework

An intelligent API automation framework that eliminates manual test scripting by using LLMs to generate and execute end-to-end business flows directly at the API level.

## How It Works
```
Swagger → API Store → Actions Store → LLM reads NL intent → Executes flow
```

1. **Swagger-driven store generation** — reads OpenAPI spec and auto-generates an action store, no manual mapping
2. **NL to actions** — LLM reads a plain English test intent and decides which API actions to execute
3. **Flow execution** — executor resolves dependencies, manages context, and runs the flow end-to-end

## Setup

1. Clone the repo and activate virtual environment:
```powershell
   .\venv\Scripts\Activate.ps1
```

2. Install dependencies:
```bash
   pip install -r requirements.txt
```

3. Create a `.env` file in the project root:
```
   BASE_URL=http://127.0.0.1:8000
   OLLAMA_URL=http://localhost:11434
   OLLAMA_MODEL=llama3.2
   SWAGGER_URL=http://127.0.0.1:8000/openapi.json
```

4. Start Ollama with llama3.2 and your target API server.

## Run
```bash
python main.py
```

## Project Structure
```
ai-automation/
├── ai/                  # LLM client and agent
├── api_store/           # Swagger parsing, store builders
├── client/              # HTTP client
├── core/                # Executor, resolver, context
├── input/               # NL intent file (nl.txt)
└── main.py              # Entry point
```

## Tech Stack

- Python, FastAPI, Ollama (llama3.2), Pydantic, pytest, requests