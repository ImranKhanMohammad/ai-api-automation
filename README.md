# AI-Powered API Automation Framework

Engineers spend more time maintaining automation than writing tests.
Every API change breaks scripts. Every new endpoint needs new code.
UI automation is slow, brittle, and avoidable for most business flows.

**This framework eliminates that.**

Describe what to test in plain English. The system reads your Swagger, understands your APIs, generates and executes the flow — without a single hardcoded request.

---

## How It Works

```
DESIGN TIME
Swagger → API Store → Actions Store → Agent Memory (real data, pre-loaded)

RUNTIME
Plain English intent → LLM → Flow → Engine → Report
                                       ├── Resolve Actions
                                       ├── Build Payload  (LLM + Agent Memory)
                                       ├── Apply Overrides
                                       ├── Execute → HTTP
                                       ├── Manage Context
                                       └── Validate (GET-based)
```

1. **Swagger-driven store generation** — reads OpenAPI spec, auto-generates API Store and Actions Store. No manual mapping.
2. **NL to actions** — LLM reads plain English test intent and maps it to executable actions.
3. **Flow execution** — engine resolves dependencies, manages context across steps, runs end-to-end.

---

## Core Principle

Generate **data** (JSON stores), not **code** (functions).

API changes → re-run builder → stores update → executor never changes.

---

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

---

## Run

```bash
python main.py
```

---

## Project Structure

```
ai-automation/
├── ai/              # LLM client and agent
├── api_store/       # Swagger parsing, store builders
├── client/          # HTTP client
├── core/            # Executor, resolver, context
├── input/           # Plain English intent (nl.txt)
└── main.py          # Entry point
```

---

## Tech Stack
Python · Ollama (llama3.2) / Claude API · FastAPI · Pydantic · requests · pytest

---

## Status
V1 in progress — REST API automation with Swagger-driven store generation.