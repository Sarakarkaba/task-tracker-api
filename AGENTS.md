# Repository Instructions

## Project purpose

This is a learning-project Task Tracker consisting of:

- A Python 3.11 FastAPI REST API.
- An in-memory task store.
- A browser-based Kanban frontend written in vanilla HTML, CSS, and JavaScript.
- Pytest API tests.
- A Docker image that runs the API only.

The API supports task creation, listing, retrieval, partial updates, deletion,
search, filtering, status-transition validation, and health reporting. The
frontend supports a three-column Kanban board, task editing, drag-and-drop
status changes, due dates, overdue filtering, search, and combined filters.

Module 5 work is focused on grading and governing AI-assisted work. Do not
treat Module 5 requests as authorization to add application features.

Sources: `README.md`, `app/main.py`, `app/storage.py`,
`frontend/index.html`, and `test/test_tasks.py`.

## Module 5 working guardrails

- Work on one bounded task per Codex thread.
- Start with read-only repository analysis.
- Prefer documentation and governance work before implementation work.
- By default, edit only files under `docs/`.
- Do not edit `app/` unless the user explicitly approves one specific,
  minimal application fix.
- Do not edit other paths unless the user explicitly approves the path and
  scope. A direct request to create or update this root `AGENTS.md` counts as
  approval for that file only.
- Before acting, briefly state:
  1. The bounded task being handled.
  2. The files that will be inspected.
  3. Whether permission is needed for any edit.
- Do not expand a review, grading, or diagnosis request into implementation
  without explicit authorization.
- Preserve unrelated user changes and untracked files.

## Repository map

- `app/main.py`: FastAPI application, CORS configuration, and route handlers.
- `app/models.py`: Pydantic request and response models, enums, defaults, and
  title validation.
- `app/storage.py`: In-memory persistence, updates, deletion, search, and
  filtering.
- `app/business_rules.py`: Allowed task-status transitions.
- `frontend/index.html`: Vanilla browser Kanban application.
- `test/`: Pytest fixtures, API tests, and a standalone model-verification
  script.
- `docs/midcourse/`: Course notes and architecture decisions.
- `.github/workflows/ci.yml`: Python 3.11 CI test workflow.
- `requirements.txt`: Pinned Python application and test dependencies.
- `Dockerfile`: Multi-stage, non-root API container.

## Confirmed technology stack

- Python 3.11.
- FastAPI 0.115.12.
- Uvicorn 0.34.2.
- Pydantic 2.11.4 and pydantic-settings 2.9.1.
- python-dotenv 1.1.0.
- pytest 8.4.2 and HTTPX 0.28.1 for testing.
- Vanilla HTML, CSS, and JavaScript for the frontend.
- In-memory Python dictionary storage; no database is used.
- Docker uses a multi-stage `python:3.11-slim` build and runs the API as the
  non-root `app` user.

Sources: `requirements.txt`, `Dockerfile`, `.github/workflows/ci.yml`,
`app/storage.py`, and `frontend/index.html`.

## Confirmed setup, run, and test commands

Run commands from the repository root.

Create and activate a virtual environment on PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```console
python -m pip install -r requirements.txt
```

Run the API locally:

```console
uvicorn app.main:app --reload --port 8000
```

Run the frontend from a second terminal:

```console
python -m http.server 5500 --directory frontend
```

The frontend expects the API at `http://localhost:8000`. The backend CORS
configuration permits `http://localhost:5500`.

Run the full test suite:

```console
pytest -v
```

Run the task API tests:

```console
pytest test/test_tasks.py -v
```

Build and run the API container:

```console
docker build -t task-tracker:dev .
docker run --rm --name tt-dev -p 8000:8000 task-tracker:dev
```

Sources: `README.md`, `.github/workflows/ci.yml`, `app/main.py`,
`frontend/index.html`, and `Dockerfile`.

No lint, formatting, static-analysis, type-checking, packaging, database
migration, frontend build, or deployment command is confirmed by the
inspected repository. Mark such commands as **not confirmed** unless new
repository evidence is found.

## Confirmed business rules

### Task values and defaults

- Status values are exactly `ToDo`, `InProgress`, and `Done`.
- Priority values are exactly `Low`, `Medium`, and `High`.
- A newly created task defaults to:
  - Status: `ToDo`
  - Priority: `Medium`
  - Description: empty string
  - Assignee: `null`
  - Due date: `null`
- Task IDs are generated UUID strings.
- Creation and update timestamps use UTC.
- Unknown request-model fields are rejected.

Source: `app/models.py`, `app/storage.py`, and `test/test_tasks.py`.

### Title validation

- A title is required when creating a task.
- Leading and trailing title whitespace is removed.
- A title must not be blank after trimming.
- A title must not exceed 200 characters.
- The same normalization and validation applies when a title is updated.
- Validation failures return HTTP `422` through FastAPI/Pydantic.

Source: `app/models.py` and `test/test_tasks.py`.

### Status transitions

The only permitted status changes are:

- `ToDo -> InProgress`
- `InProgress -> Done`
- `Done -> InProgress`

All other status changes are invalid, including changing a task to its current
status. Invalid transitions return HTTP `422`.

Source: `app/business_rules.py`, `app/main.py`, and `test/test_tasks.py`.

### Updates and persistence

- `PATCH /tasks/{task_id}` performs partial updates.
- Fields omitted from a patch retain their current values.
- An explicitly supplied `null` description is stored as an empty string.
- An explicitly supplied `null` due date removes the due date.
- If supplied values do not change the task, the existing task is returned
  without changing `updated_at`.
- Data is stored only in process memory and is lost when the application
  restarts.
- Missing task IDs return HTTP `404` for retrieval, update, and deletion.

Source: `app/main.py`, `app/storage.py`, and `test/test_tasks.py`.

### Search and filtering

- Search is case-insensitive and matches substrings in titles or descriptions.
- A whitespace-only search is treated as no search.
- Assignee filtering is case-insensitive, trimmed, and exact.
- Status, priority, and due-date filters use exact matches.
- Multiple active backend filters use AND logic.

Source: `app/storage.py` and `test/test_tasks.py`.

### Frontend-only behavior

- The Kanban columns use `ToDo`, `InProgress`, and `Done`.
- Tasks are ordered by priority: High, then Medium, then Low.
- A task is overdue when its due date is earlier than the browser's local
  calendar date and its status is not `Done`.
- Overdue-only filtering is performed in the frontend, not by the API.

Source: `frontend/index.html` and `docs/midcourse/mini-adr.md`.

## Security and governance

- Never paste, expose, log, or commit secrets, tokens, credentials, private
  keys, environment-file contents, or sensitive user data.
- Do not assume that a file is safe to expose because it is present locally.
- Do not run destructive commands, including forced deletion, history
  rewriting, broad cleanup, or destructive database/container operations.
- Do not overwrite, revert, stage, commit, push, or delete user work unless
  the user explicitly requests that exact action.
- Inspect the working tree before edits and preserve unrelated changes.
- Support repository claims with paths to files actually inspected.
- Distinguish code evidence, test evidence, documentation claims, and personal
  inference.
- If a relevant file is missing, inaccessible, ambiguous, or not inspected,
  say so.
- Never invent commands, test results, business rules, vulnerabilities,
  findings, or implementation details.
- Mark unsupported or unverified statements as **not confirmed**.
- Do not claim tests passed unless they were run successfully in the current
  task; report the exact command used when tests are run.
- Prefer the smallest read-only checks needed to answer the bounded question.
