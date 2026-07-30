# Prompt Log

---

# Feature 1: Due Dates and Overdue Filter

## Prompt 1 – Generate User Stories

### Prompt

> Add a "Due Dates and Overdue Filter" feature to the Task Tracker. Write five user stories. Each story must include acceptance criteria and identify at least one AI assumption that was corrected.

### AI Response

AI generated user stories for:

- assigning due dates
- updating/removing due dates
- displaying due dates
- highlighting overdue tasks
- filtering overdue tasks

### My Review

**Accepted**

- Due dates are optional.
- Completed tasks are never overdue.
- Tasks due today are not overdue.

**Edited**

- Rewrote the stories to make every acceptance criterion specific and testable.

**Rejected**

- Displaying "No due date" on every task card because it adds unnecessary visual clutter.

---

## Prompt 2 – Backend Implementation

### Prompt

> Implement only the backend changes for Due Dates. Add an optional `due_date` field to the existing models, persist it in the in-memory storage, support clearing it with `null`, reject invalid dates with HTTP 422, and generate focused pytest tests. Do not modify frontend files.

### AI Response

AI updated:

- Pydantic models
- storage helpers
- backend validation
- pytest tests

### My Review

**Accepted**

- ISO date support
- `null` for removing due dates
- Backend tests

**Edited**

- Restricted the implementation to backend files only.

**Rejected**

- Database migrations because the project uses in-memory storage.

---

## Prompt 3 – Frontend Implementation

### Prompt

> Update only `frontend/index.html`. Add an optional due-date field, display due dates on task cards, highlight overdue tasks, and add an overdue filter. Preserve drag-and-drop, priority sorting, and existing board states.

### AI Response

AI added:

- HTML date input
- overdue badge
- local overdue calculation
- overdue filter

### My Review

**Accepted**

- Native date input
- Overdue highlighting
- Client-side filtering

**Edited**

- Updated the API URL to match the existing project.

**Rejected**

- External date libraries
- Frontend frameworks

---

## Weak Prompt → Improved Prompt

### Weak Prompt

> Implement this feature.

### Why it was weak

The prompt did not define:

- project scope
- affected files
- validation rules
- behaviors to preserve

### Improved Prompt

> Implement the Due Dates feature in two steps. First update only the FastAPI models, storage, and tests. After the backend passes, update only `frontend/index.html` with the due-date field, overdue highlighting, and overdue filter. Preserve drag-and-drop, priority sorting, and existing UI states. Do not add dependencies or new endpoints.

### Result

The AI generated smaller, focused changes that were easier to inspect and verify before moving to the next step.

---

# Feature 2: Search and Combined Filters

## Prompt 1 – Define Search Behaviour

### Prompt

> Extend the Task Tracker with search and combined filters. Generate user stories covering text search, status, priority, assignee, due date, and combined filtering.

### AI Response

AI proposed stories for:

- text search
- field filtering
- due-date filtering
- combined filters

### My Review

**Accepted**

- Search title and description.

**Edited**

- Changed combined filtering to use **AND** logic.

**Rejected**

- Searching task IDs.
- Partial assignee matching.

---

## Prompt 2 – Backend Implementation

### Prompt

> Extend only the existing `GET /tasks` endpoint. Add optional query parameters for `search`, `status`, `priority`, `assignee`, and `due_date`. Combine all backend filters using AND logic. Return HTTP 200 with an empty list when no tasks match. Keep overdue-only filtering client-side and do not add an `overdue` query parameter. Do not modify frontend files.

### AI Response

AI extended the existing endpoint with filtering logic and generated backend tests.

### My Review

**Accepted**

- Reusing the existing endpoint.
- Combined filtering.

**Edited**

- Simplified the filtering logic for readability.

**Rejected**

- Creating separate endpoints for every filter.
- Adding a backend `overdue` filter because overdue-only filtering already exists in the frontend.

---

## Prompt 3 – Frontend Implementation

### Prompt

> Update only `frontend/index.html`. Add a search and filter bar above the Kanban board. Support text search, status, priority, assignee, due date, and overdue filters while preserving drag-and-drop, priority sorting, and board states.

### AI Response

AI added:

- search bar
- filter controls
- frontend filtering

### My Review

**Accepted**

- Compact filter controls
- Board refresh

**Edited**

- Added a clear/reset action to restore the full board.

**Rejected**

- Live search suggestions.
- Advanced search syntax.

---

## Weak Prompt → Improved Prompt

### Weak Prompt

> Add search to the board.

### Why it was weak

It did not specify:

- search fields
- filter behavior
- backend endpoint
- preserved functionality

### Improved Prompt

> Extend only the existing `GET /tasks` endpoint and `frontend/index.html`. Add a `search` query parameter for title and description text, plus backend filters for status, priority, assignee, and due date. Combine these backend filters using AND logic. Keep the existing overdue-only filter client-side rather than adding an `overdue` query parameter. Preserve drag-and-drop, priority sorting, and all board states. Do not introduce new endpoints, frameworks, or unrelated features.

### Result

The AI generated focused backend and frontend changes that fit cleanly into the existing project and were easy to verify.
