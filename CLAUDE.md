# Task Tracker

## Stack
- Python 3.10+
- FastAPI + Pydantic v2 + Uvicorn
- pytest + httpx for tests
- Vanilla JavaScript frontend in frontend/index.html

## Run
- Install: `.\venv\Scripts\python.exe -m pip install -r requirements.txt`
- Server: `.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000`
- Tests: `.\venv\Scripts\python.exe -m pytest -q`
- Single test: `.\venv\Scripts\python.exe -m pytest test/test_tasks.py::test_create_task_valid_returns_201_with_full_body -v`
- Frontend: `.\venv\Scripts\python.exe -m http.server 5500 --directory frontend`, then open `http://localhost:5500`

## Architecture
- app/main.py: FastAPI app, dotenv loading, CORS middleware, health endpoint, and task route handlers
- app/models.py: Pydantic schemas and validation types
- app/storage.py: in-memory task store, CRUD functions, search, and filters
- app/business_rules.py: status transition validation
- test/: pytest fixtures and API tests; verify_a.py is a standalone model-verification script
- frontend/index.html: Kanban board UI from Module 3

## Business rules that must not be violated
- Valid transitions: ToDo -> InProgress, InProgress -> Done, Done -> InProgress
- Invalid transitions: ToDo -> Done, Done -> ToDo, same status -> same status
- Invalid transitions return 422
- Task creation requires a title; titles are trimmed, non-empty, and at most 200 characters
- Frontend must keep loading, empty, error, and populated states
- Frontend status values must stay ToDo, InProgress, Done

## Do not
- Do not add authentication
- Do not introduce a database without asking
- Do not change public response shapes without explicit approval
- Do not remove tests to make CI pass
- Do not run destructive shell commands without explicit confirmation
- Do not use always allow for broad shell permissions

@README.md
