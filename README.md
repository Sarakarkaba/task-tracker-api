# Module 4 Task Tracker

A learning project for the AI-Assisted Coding. It
combines a Python 3.11 FastAPI backend with a browser-based Kanban board built
with vanilla HTML, CSS, and JavaScript.

The API supports:

- Creating, listing, retrieving, updating, and deleting tasks.
- Searching task titles and descriptions.
- Filtering by status, priority, assignee, and due date.
- Validating task titles and status transitions.
- Reporting application health through `GET /health`.

The frontend adds task editing, drag-and-drop status changes, due dates,
overdue filtering, text search, and combined filters.

## API behavior

| Method | Route | Success | Errors |
|---|---|---|---|
| `GET` | `/health` | `200` with `status` and a UTC timestamp | None |
| `POST` | `/tasks` | `201` with a `TaskResponse` body | `422` for request validation errors |
| `GET` | `/tasks` | `200` with a list of tasks | `422` for invalid query parameters |
| `GET` | `/tasks/{task_id}` | `200` with a `TaskResponse` body | `404` when the task does not exist |
| `PATCH` | `/tasks/{task_id}` | `200` with the updated task | `404` when the task does not exist; `422` for request validation or an invalid status transition |
| `DELETE` | `/tasks/{task_id}` | `204` with no response body | `404` when the task does not exist |

FastAPI and Pydantic request-validation errors use HTTP `422` with a list in
the response's `detail` field. Invalid status transitions also use HTTP `422`,
but return a human-readable string in `detail`.

## Prerequisites

- Python 3.11
- `pip`
- Docker Desktop or another Docker-compatible runtime for container commands
- GitHub access if you want to inspect CI runs

Run all commands below from the repository root.

## Local setup

Create a virtual environment.

PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the pinned application and test dependencies:

```console
python -m pip install -r requirements.txt
```

## Run the app locally

Activate the virtual environment, then start the FastAPI development server:

```console
uvicorn app.main:app --reload --port 8000
```

The backend is available at:

- API: `http://localhost:8000`
- Health endpoint: `http://localhost:8000/health`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

To use the Kanban frontend, keep the backend running and start a static file
server in a second terminal:

```console
python -m http.server 5500 --directory frontend
```

Open `http://localhost:5500`. The port must remain `5500` because the API
currently permits the CORS origin `http://localhost:5500`.

## Run tests

With the virtual environment active, run the complete test suite:

```console
pytest -v
```

Run only the task API tests:

```console
pytest test/test_tasks.py -v
```

## Run with Docker

Build the multi-stage Python 3.11 slim image:

```console
docker build -t task-tracker:dev .
```

Start the API in a container and map port `8000`:

```console
docker run --rm --name tt-dev -p 8000:8000 task-tracker:dev
```

In another PowerShell terminal, verify the mapped health endpoint:

```powershell
Invoke-RestMethod http://localhost:8000/health
```

Expected output includes a status of `ok` and a UTC timestamp.

The container runs as the non-root user `app`. It does not run Uvicorn with
automatic reload, and it does not include the frontend.

Press `Ctrl+C` in the container terminal to stop it. If a stopped or existing
container prevents reuse of the name, remove it:

```console
docker rm -f tt-dev
```

## CI workflow summary

The GitHub Actions workflow in `.github/workflows/ci.yml` runs for pushes and
pull requests. It:

1. Checks out the repository on `ubuntu-latest`.
2. Installs Python 3.11.
3. Installs dependencies from `requirements.txt`.
4. Runs `pytest -v` with the repository root on `PYTHONPATH`.

The workflow tests the Python project. It does not deploy the application,
publish a Docker image, or configure a production environment.

## Project structure

```text
.
|-- app/
|   |-- main.py             # FastAPI application and route handlers
|   |-- models.py           # Pydantic request and response models
|   |-- storage.py          # In-memory task storage and filtering
|   `-- business_rules.py   # Allowed task status transitions
|-- frontend/
|   `-- index.html          # Vanilla JavaScript Kanban interface
|-- test/
|   |-- conftest.py         # Shared pytest fixtures
|   |-- test_tasks.py       # API behavior tests
|   `-- verify_a.py         # Standalone model verification script
|-- docs/
|   `-- midcourse/          # Project notes and learning artifacts
|-- .github/
|   `-- workflows/
|       `-- ci.yml          # Push and pull-request test workflow
|-- Dockerfile              # Multi-stage non-root container image
|-- .dockerignore           # Docker build-context exclusions
|-- requirements.txt        # Pinned Python dependencies
`-- README.md
```

## Project conventions and current limitations

- Task statuses are `ToDo`, `InProgress`, and `Done`.
- Valid transitions are `ToDo -> InProgress`, `InProgress -> Done`, and
  `Done -> InProgress`.
- Invalid transitions, including transitions to the same status, return HTTP
  `422`.
- Titles are trimmed, must not be blank, and must not exceed 200 characters.
- Search is case-insensitive across task titles and descriptions.
- Multiple active backend filters use AND logic.
- Overdue status is calculated by the frontend using the browser's local
  calendar date.
- Data is held in memory and is lost whenever the application restarts.
- The project has no database, authentication, authorization, or deployment
  configuration.
- The Docker image contains the API only; it does not serve the frontend.
- CORS is currently limited to `http://localhost:5500` and the configured
  methods `GET`, `POST`, and `PATCH`.
- This is a course project and is not presented as production-ready.

## Technical note

- [In-Memory Task Storage](docs/decisions/in-memory-task-storage.md) explains
  why the project uses process-local storage and records the alternatives,
  trade-offs, consequences, and open questions.
- [Mini Architecture Decision Record](docs/midcourse/mini-adr.md) records
  decisions about due dates, overdue filtering, search, and combined filters.
