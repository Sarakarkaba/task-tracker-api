# Comments on Tasks: Feature Plan

**Status:** Proposed; plan only, with no implementation.

The document follows the Module 5 exercise order: construct the generic plan
first, create the repo-grounded plan second, then critique and compare them.

## Step 1 - Generic Plan

This plan uses only the feature description and common web-application
assumptions. Repository evidence is introduced later in Step 2.

| Area | Generic proposal |
|---|---|
| Data model | Add a persisted `Comment` entity related to a task, with UUID, author, body, and creation timestamp fields. |
| API | Add nested create, list, update, and delete comment endpoints with validation and missing-resource errors. |
| Tests | Cover model validation, endpoint success and failure cases, permissions, and comment deletion. |
| Frontend | Add a comments component to a task-details view with loading, empty, submission, and error states. |
| Migration | Create a comments table, task foreign key, and task-indexed query path. |
| Open questions | Decide authentication, editing, deletion, ordering, and pagination rules. |

## Step 2 - Repo-Grounded Plan

### 1. Data Model

Add these models to `app/models.py`, following the existing task-model pattern:

- `CommentCreate`: required `author` of 1-100 characters and required `body`
  of 1-2,000 characters. Reject unknown and server-managed fields with
  `ConfigDict(extra="forbid")`.
- `CommentResponse`: string UUID `id`, parent `task_id`, `author`, `body`, and
  server-generated UTC `created_at`.

Store comments in a separate in-memory dictionary in `app/storage.py`, keyed
by comment ID. Validate `task_id` against the existing task store, generate IDs
and timestamps in storage, and clear comments in `_reset()`.

### 2. API Routes

Add the routes to `app/main.py`:

| Method and path | Request | Success | Errors |
|---|---|---|---|
| `POST /tasks/{task_id}/comments` | `CommentCreate` | `201` with `CommentResponse` | `404` for a missing task; `422` for invalid input |
| `GET /tasks/{task_id}/comments` | None | `200` with `list[CommentResponse]`; an empty list when the task has no comments | `404` for a missing task |

The task ID comes from the path, not the body. The existing frontend CORS
configuration already permits `GET` and `POST`.

### 3. Tests

Add `test/test_comments.py`, using the existing `client` and `created_task`
fixtures.

#### Happy path

- `test_create_comment_returns_201_with_server_fields`
- `test_list_comments_returns_oldest_first`
- `test_list_comments_for_task_without_comments_returns_empty_list`
- `test_list_comments_returns_only_requested_task_comments`

#### Validation

- `test_create_comment_requires_author_and_body`
- `test_create_comment_rejects_empty_values`
- `test_create_comment_enforces_length_limits`
- `test_create_comment_rejects_unknown_and_server_managed_fields`

#### Edge cases

- `test_create_comment_for_missing_task_returns_404`
- `test_list_comments_for_missing_task_returns_404`
- `test_storage_reset_clears_comments`
- `test_delete_task_handles_associated_comments` after the deletion policy is
  decided

### 4. Frontend Changes

Update only `frontend/index.html`:

- Show comments when editing an existing task; hide them during task creation.
- Load and render comments with loading, empty, and error states.
- Add required author and body fields with the same backend length limits.
- Submit new comments without closing the task modal.
- Render user text with `textContent` and reuse `getServerErrorMessage()`.
- Document the two routes and chosen comment rules in `README.md`.

### 5. Migration Notes

No database migration is needed because the project uses process-local memory.
Keep comments separate so existing task responses remain unchanged. Update
`_reset()` for test isolation. Decide whether deleting a task should delete its
comments before implementation.

### 6. Open Questions

1. Should `author` and `body` be trimmed and reject whitespace-only values?
2. Are comments immutable, or will editing and deletion be added later?
3. Should task deletion cascade-delete comments?
4. Should comments be oldest-first, and is pagination needed?
5. Should comments appear in the existing task modal or a separate view?

### Files Read

- `AGENTS.md`
- `app/models.py`
- `app/main.py`
- `app/storage.py`
- `app/business_rules.py`
- `test/conftest.py`
- `test/test_tasks.py`
- `frontend/index.html`
- `README.md`

### Assumptions to Verify

- Initial scope includes creating and listing comments only.
- Comments are stored separately and do not change `TaskResponse`.
- A task with no comments returns `200` with an empty list.
- Comments are returned oldest first.
- The existing task modal is the intended frontend location.

## Step 3 - Tech-Lead Critique

| Section | Label | Evidence | Minimal correction |
|---|---|---|---|
| Data Model | Right | Follows the existing Pydantic and in-memory storage patterns. | Resolve normalization and mutability first. |
| API Routes | Right | Names concrete routes, bodies, status codes, and errors. | Confirm the final comment rules. |
| Tests | Needs-Resequencing | Tests are concrete, but some depend on unresolved rules. | Decide normalization, deletion, and ordering before finalizing tests. |
| Frontend Changes | Right | Uses the actual single-file frontend and existing helpers. | Confirm the comment placement. |
| Migration Notes | Right | Correctly avoids inventing a database migration. | Confirm the deletion policy. |
| Open Questions | Needs-Resequencing | The questions affect models, routes, and tests. | Resolve the blocking questions before implementation. |

## Step 4 - Generic vs Repo-Grounded Comparison

- **Biggest difference:** The generic plan assumes a database, extra CRUD
  routes, permissions, and separate frontend components; the grounded plan
  uses the actual in-memory store, create/list scope, existing fixtures, and
  single-file frontend.
- **Plan I would hand to a teammate:** The grounded plan, because its files,
  constraints, tests, and assumptions can be verified in this repository.
- **When generic chat is enough:** Early brainstorming before
  repository-specific design and sequencing begin.
