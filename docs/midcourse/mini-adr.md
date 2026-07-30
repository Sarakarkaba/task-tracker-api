# Mini Architecture Decision Record

**Status:** Accepted

## Context

The project extends the existing Task Tracker with two small end-to-end features:

1. Due Dates and Overdue Filter
2. Search and Combined Filters

The implementation must remain consistent with the existing FastAPI backend, in-memory storage, and vanilla HTML, CSS, and JavaScript frontend. The solution should reuse the current architecture rather than introducing new frameworks, databases, or unnecessary complexity.

---

# Feature 1: Due Dates and Overdue Filter

## Decision

- Add an optional `due_date` field to the existing `TaskCreate`, `TaskUpdate`, and `TaskResponse` models.
- Represent due dates as ISO calendar dates (`YYYY-MM-DD`), with `null` meaning no due date.
- Reuse the existing in-memory task storage and current `POST /tasks` and `PATCH /tasks/{id}` routes.
- Add a native HTML date input to the existing create/edit modal.
- Compute overdue status in the frontend using the browser's local calendar date.
- A task is overdue when its due date is earlier than today and its status is not `Done`.
- Add a client-side overdue filter while preserving the existing three-column Kanban layout and priority ordering.

## Alternatives AI Suggested

- Store full date-time values with time zones.
- Add an `overdue=true` backend query parameter.
- Store an `is_overdue` field on each task.
- Introduce a third-party date library.

## Rejected

- Time-zone support was unnecessary for simple day-level deadlines.
- A backend `overdue=true` query parameter was unnecessary because overdue status is calculated from the browser's local calendar date and filtered in the frontend.
- A stored `is_overdue` value could become stale as the date changes.
- A date library was unnecessary because native HTML date inputs and ISO dates provide sufficient functionality.
- Additional backend endpoints or persistence changes were outside the intended project scope.

## Consequences

The implementation remains lightweight, dependency-free, and consistent with the existing architecture while providing clear visual feedback for overdue tasks.

---

# Feature 2: Search and Combined Filters

## Decision

- Extend the existing `GET /tasks` endpoint to support optional filtering parameters.
- Support text search across task titles and descriptions.
- Support backend filtering by status, priority, assignee, and due date. Overdue-only filtering remains client-side.
- Apply all active filters using AND logic.
- Keep all three Kanban columns visible even when filters produce empty columns.
- Reuse the existing frontend task rendering without introducing additional state-management libraries.

## Alternatives AI Suggested

- Create separate endpoints for each filter.
- Add advanced search syntax with Boolean operators.
- Introduce server-side pagination and sorting.
- Add a dedicated search engine or indexing library.

## Rejected

- Separate endpoints would duplicate existing functionality.
- Advanced search syntax was unnecessary for the project scope.
- Pagination and indexing would add complexity without improving the learning objectives.
- Additional libraries or persistence mechanisms were outside the scope of the assignment.

## Consequences

Filtering remains simple, predictable, and easy to maintain. The implementation supports multiple filter combinations while keeping both the backend and frontend small and consistent with the existing project architecture.
