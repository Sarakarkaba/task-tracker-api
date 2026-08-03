# Task Tracker Architecture and Context-Strategy Comparison

## Purpose and Scope

The Task Tracker is a learning project with two independently served parts: a
FastAPI REST API and a browser-based Kanban frontend written in vanilla HTML,
CSS, and JavaScript. The backend stores tasks in process memory. There is no
database, authentication, deployment platform, or frontend build system.

This document has two purposes. First, it records the final architecture I
verified from the repository. Second, it explains why I chose structured
context over minimal or narrowly targeted context when asking AI to describe
the whole system.

## System Overview

```text
Browser at localhost:5500
  frontend/index.html
          |
          | HTTP + JSON
          v
FastAPI at localhost:8000
  app/main.py
     |             |
     v             v
business rules   models and validation
     |             |
     +------v------+
            |
            v
  in-memory task dictionary
      app/storage.py
```

The frontend calls the API directly at `http://localhost:8000`. CORS permits
the local frontend origin, `http://localhost:5500`, for `GET`, `POST`, and
`PATCH`. The API also exposes a `DELETE` route, but the current frontend has no
delete action and sends no `DELETE` request. This is a deliberate description
of the current client, not a claim that the API lacks deletion.

## Main Components

| Component | Responsibility | Evidence |
|---|---|---|
| FastAPI application | Configures CORS and exposes health and task routes. | [`app/main.py`](../app/main.py) |
| Request and response models | Defines task fields, enums, defaults, title validation, and unknown-field rejection. | [`app/models.py`](../app/models.py) |
| Business rules | Defines and validates the allowed task-status transitions. | [`app/business_rules.py`](../app/business_rules.py) |
| In-memory storage | Creates UUIDs and UTC timestamps and performs retrieval, updates, deletion, search, and filtering. | [`app/storage.py`](../app/storage.py) |
| Kanban frontend | Renders the board, edits tasks, changes status by drag and drop, and applies browser-only presentation rules. | [`frontend/index.html`](../frontend/index.html) |
| API tests | Exercises task creation, validation, retrieval, filtering, transitions, updates, and deletion. | [`test/test_tasks.py`](../test/test_tasks.py) |
| CI workflow | Installs the pinned requirements under Python 3.11 and runs `pytest -v` on pushes and pull requests. | [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) |
| API container | Builds a Python 3.11 API image, runs as the non-root `app` user, and checks `/health`. | [`Dockerfile`](../Dockerfile) |

## Task Model and Business Rules

A task contains an ID, title, description, status, priority, assignee, due
date, creation timestamp, and update timestamp. New tasks default to `ToDo`
status, `Medium` priority, an empty description, and no assignee or due date.
The storage layer generates UUID strings and UTC timestamps.

Titles are trimmed, must not be blank, and must not exceed 200 characters.
Unknown request fields are rejected. The status values are exactly `ToDo`,
`InProgress`, and `Done`; priorities are exactly `Low`, `Medium`, and `High`.

The allowed status transitions are:

- `ToDo -> InProgress`
- `InProgress -> Done`
- `Done -> InProgress`

Changing a task to its current status is not an allowed transition. The
frontend avoids that error during ordinary edits by omitting `status` when it
has not changed.

## API and Request Flow

| Method and path | Purpose | Successful response | Important failure behavior |
|---|---|---|---|
| `GET /health` | Report API health and a UTC timestamp. | `200` | No repository-specific failure response. |
| `POST /tasks` | Validate, create, and store a task. | `201` with the stored task. | Invalid input returns `422`. |
| `GET /tasks` | List, search, and filter tasks. | `200` with a list. | Invalid enum or date filters return `422`. |
| `GET /tasks/{task_id}` | Retrieve one task. | `200` with the task. | A missing ID returns `404`. |
| `PATCH /tasks/{task_id}` | Partially update one task. | `200` with the updated or unchanged task. | A missing ID returns `404`; an invalid transition returns `422`. |
| `DELETE /tasks/{task_id}` | Delete one task through the API. | `204` with no response body. | A missing ID returns `404`. |

The list route passes active filters to the storage layer. Search is a
case-insensitive substring match over title and description. Assignee matching
is trimmed, case-insensitive, and exact. Status, priority, and due-date filters
use exact values. When several filters are active, a task must satisfy all of
them.

PATCH requests use only fields supplied by the client. An explicit `null`
description becomes an empty string, and an explicit `null` due date removes
the date. If the supplied values do not change the task, the existing object
is returned without changing `updated_at`.

## Frontend Behavior

The browser renders three columns for `ToDo`, `InProgress`, and `Done`. It
loads task data from the API, opens a dialog for creation or editing, and
closes the dialog after a successful `POST` or `PATCH`. Drag and drop sends a
status-only PATCH request; if the request fails, the frontend restores the
previous status and displays an error.

Within each column, tasks are ordered High, Medium, then Low. The backend does
not calculate overdue status. The frontend marks a task overdue when its due
date is earlier than the browser's local calendar date and the task is not
`Done`. The overdue-only option is therefore applied in the browser after the
API response, while search and the other filters are sent to the API.

## Persistence and Runtime Boundaries

The task store is a module-level Python dictionary. This keeps the course
project simple, but it also means:

- data is lost whenever the API process restarts;
- separate worker processes would not share task data;
- there is no transaction, backup, migration, or concurrency design;
- list responses have no pagination or task-count limit.

The frontend is not bundled into the Docker image. It is served separately,
for example with `python -m http.server 5500 --directory frontend`. The Docker
image contains only the API runtime, uses a multi-stage Python 3.11 slim build,
switches to the non-root `app` user, exposes port 8000, and checks `/health`.

CI runs the API test suite on pushes and pull requests. It verifies the Python
application but does not build the Docker image, run browser automation,
publish an artifact, or deploy the project.

## Known Limitations and Production Boundaries

This architecture is appropriate for the local learning goals, but I would
not describe it as production-ready. The most important boundaries are:

- task routes have no authentication, authorization, or ownership checks;
- storage is process-local and temporary;
- description and assignee lengths, task count, and list size are unbounded;
- explicit `null` values for required PATCH response fields (`title`,
  `status`, and `priority`) currently produce HTTP `500` instead of a
  controlled validation response;
- the frontend API URL and CORS origin are fixed for the local HTTP workflow;
- the runtime image includes test dependencies because application and test
  packages share one requirements file;
- no external dependency scan or production deployment configuration is part
  of the repository.

These are documented constraints and backlog items, not authorization to add
features during Module 5.

## Context-Strategy Comparison

I compared three ways of giving AI repository context before accepting a
system description. I checked the drafts against the source files rather than
using agreement between drafts as proof.

| Strategy | What it got right | What it got wrong or missed | Best-suited task shape |
|---|---|---|---|
| **A - Minimal context** | Produced a readable overview of the application purpose, task model, main files, in-memory storage, validation, transitions, and frontend/backend split. Its claims that creation closes the dialog, API deletion returns `204`, and Docker uses a multi-stage build are all confirmed by the repository. | Missed CI, unchanged-update behavior, combined-filter logic, and browser-side priority ordering. It also claimed the frontend supports deletion, but only the API exposes deletion. | Fast orientation or a low-risk summary where brevity matters more than complete traceability. |
| **B - Structured context** | Covered the backend, frontend, tests, CI, container, storage, validation, transitions, filters, updates, and browser-only behavior. Its CI, AND-filter, unchanged-timestamp, and priority-ordering claims are confirmed by the relevant files. | Also described frontend deletion, which the current browser client does not implement. It used "optional description" without clearly separating omission, the empty-string default, and explicit `null` normalization. It needed more direct source references. | Repository-wide architecture, onboarding, and governance work spanning several layers. |
| **C - Targeted context** | Gave the most precise backend request flow and clearly identified model roles, title validation, UUID and timestamp creation, null-description normalization, storage, filtering, and CORS. It was careful about evidence boundaries. | Was intentionally too narrow for a complete architecture: it left frontend behavior, transitions, tests, dependencies, CI, and Docker unresolved. It correctly noticed that CORS excludes `DELETE`, but that is not a current frontend conflict because the browser client does not delete tasks. | Focused endpoint tracing, diagnosis, or review where a small set of authoritative files should bound every claim. |

## My Verdict

I chose **Strategy B - structured context** as the starting point for this
final architecture document because the system crosses API, browser, testing,
CI, and container boundaries. It gave me the best overall coverage. I still
had to borrow Strategy C's discipline: every important claim needed a source,
and a confident statement was not enough on its own.

The biggest correction was frontend deletion. Two broad drafts repeated it,
but the actual browser code never sends a `DELETE` request. That was a useful
reminder that agreement between AI outputs is not independent verification.

## My Context-Engineering Rule

For a repository-wide document, I use structured context so the explanation
does not lose an entire layer such as CI or the frontend. For a narrow request
flow or bug, I use targeted context because fewer authoritative files make it
easier to trace each claim. In both cases, I treat the generated explanation
as a draft until I check it against the repository.
