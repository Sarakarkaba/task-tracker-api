# Task Tracker

Task Tracker is an AI-Assisted Coding course project that combines a Python
FastAPI REST API with a browser-based Kanban board built in vanilla HTML, CSS,
and JavaScript.

## Module 1 - API skeleton

The project started with a minimal FastAPI application and a `GET /health`
endpoint that established the backend structure and local development setup.

## Module 2 - Task API and tests

The backend gained task models, in-memory storage, CRUD routes, validation,
status-transition rules, and pytest coverage for the API behavior.

## Module 3 - Kanban frontend and features

The browser Kanban board added task editing, drag-and-drop status changes, due
dates, overdue display and filtering, search, combined filters, and local CORS
support.

## Module 4 - CI, Docker, and delivery

Module 4 pinned the Python 3.11 dependencies, added GitHub Actions and a
multi-stage non-root Docker image, and checked the delivery documentation
against the repository and running application.

The completed API supports:

- Creating, listing, retrieving, updating, and deleting tasks.
- Searching task titles and descriptions.
- Filtering by status, priority, assignee, and due date.
- Validating task titles and status transitions.
- Reporting application health through `GET /health`.

The frontend provides the three-column Kanban workflow described in Module 3.

### API behavior

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

### CI workflow summary

The GitHub Actions workflow in `.github/workflows/ci.yml` runs for pushes and
pull requests. It:

1. Checks out the repository on `ubuntu-latest`.
2. Installs Python 3.11.
3. Installs dependencies from `requirements.txt`.
4. Runs `pytest -v` with the repository root on `PYTHONPATH`.

The workflow tests the Python project. It does not deploy the application,
publish a Docker image, or configure a production environment.

### Project conventions and current limitations

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

### Technical note

- [In-Memory Task Storage](docs/decisions/in-memory-task-storage.md) explains
  why the project uses process-local storage and records the alternatives,
  trade-offs, consequences, and open questions.
- [Mini Architecture Decision Record](docs/midcourse/mini-adr.md) records
  decisions about due dates, overdue filtering, search, and combined filters.

## Final Project

Branch reviewed: `final-project`

### What this submission demonstrates

- Existing Task Tracker app still runs inside the intended course scope.
- CI runs the pytest suite on push and pull request.
- Docker image builds and runs with `/health` returning HTTP `200`.
- AI review, security, and ownership evidence is in `docs/`.

### How to run locally

From the repository root, create the environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Run the API:

```powershell
uvicorn app.main:app --reload --port 8000
```

From a second terminal, run the frontend:

```powershell
python -m http.server 5500 --directory frontend
```

### How to run tests

```powershell
pytest -v
```

### How to run with Docker

```powershell
docker build -t task-tracker:dev .
docker run --rm --name tt-dev -p 8000:8000 task-tracker:dev
```

From a second terminal, check container health:

```powershell
curl.exe --fail http://localhost:8000/health
```

### Evidence files

- `docs/release-evidence.md`
- `docs/final-ai-review.md`
- `docs/ai-playbook.md`

### AI assistance summary

AI helped draft and review: CI, Docker, documentation, security findings, and
debugging evidence.

I verified the work by: running tests, reviewing diffs, building and running
the Docker image, checking `/health`, and performing a manual security check.

One AI suggestion I rejected or corrected: treating the missing CORS
permission for unused `DELETE` requests as a security vulnerability.
