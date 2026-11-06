# AI API automation

Plain-English test intent goes in. The runner reads an OpenAPI spec, turns it into JSON action stores, asks a local LLM which actions match the sentence, and calls those HTTP endpoints.

The sample target is [fastapi-hr-service](https://github.com/ImranKhanMohammad/fastapi-hr-service).

## What V1 does

1. Load `SWAGGER_URL` and write API, action, and GET-response stores under `input/`.
2. Read `input/nl.txt`.
3. Ask Ollama to pick action names from the store.
4. Build each request body from the OpenAPI schema plus a real GET sample, and resolve path parameters from earlier responses.
5. Call each chosen endpoint in order and print the HTTP result.

Stores are data. The executor does not change when the API spec changes; re-run the builder.

## Quick start

Terminal 1 — sample API:

```powershell
git clone https://github.com/ImranKhanMohammad/fastapi-hr-service.git
cd fastapi-hr-service
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --port 8000
```

Terminal 2 — this repo. Ollama must already be running with `llama3.2` (`ollama pull llama3.2`).

```powershell
git clone https://github.com/ImranKhanMohammad/ai-api-automation.git
cd ai-api-automation
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
mkdir input
Set-Content input\nl.txt "create a new employee and terminate them for a future date"
python main.py
```

`.env` points at the HR service:

```
BASE_URL=http://127.0.0.1:8000
OLLAMA_URL=http://127.0.0.1:11434
OLLAMA_MODEL=llama3.2
SWAGGER_URL=http://127.0.0.1:8000/openapi.json
```

`input/` is local output and is not committed. The HR spec exposes these action names, among others: `post_employees`, `put_employees_emp_id_terminate`.

One captured run is in [examples/sample-run.txt](examples/sample-run.txt). The model chose `post_employees` then `put_employees_emp_id_terminate`. Both calls returned HTTP 200: employee Kamran was created, then terminated with `effective_date` 2026-12-06. A later run can choose different names and dates. The model is llama3.2 at temperature 0.

## Layout

```
ai/          LLM client and action picker
api_store/   OpenAPI load and store builders
client/      HTTP calls
core/        Executor, resolver, context
main.py
```

## Stack

Python, Ollama (`llama3.2`), requests, FastAPI, Pydantic.

## Status

V1 on `main`: OpenAPI to JSON stores, local LLM chooses actions, executor fills bodies and path parameters, then performs the HTTP calls. See `examples/sample-run.txt` for one passing run against fastapi-hr-service. There is no CI yet.
