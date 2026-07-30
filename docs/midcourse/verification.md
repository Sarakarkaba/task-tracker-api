# Feature 1 Verification: Due Dates and Overdue Filter

**Verification date:** 2026-07-31  
**Backend feature commit:** `c95e6b6`  
**Frontend feature commit:** `8c9362e`

## Baseline Check

The baseline was inspected from the commit immediately before the Feature 1 backend commit.

| Check | Before Feature 1 | After Feature 1 |
|---|---:|---:|
| Pytest tests collected | 23 | 27 |
| `due_date` in backend models | Not present | Present in create, update, and response models |
| Due-date API tests | 0 | 4 |
| Due-date modal field | Not present | Native optional date input |
| Overdue filter | Not present | Client-side checkbox filter |

Baseline command:

```powershell
git show c95e6b6^:test/test_tasks.py |
  Select-String -Pattern '^def test_' |
  Measure-Object
```

Result: `23` test functions. The baseline model and frontend contained no `due_date` or overdue-filter implementation.

## Backend Test Results

Full-suite command:

```powershell
.\venv\Scripts\python.exe -m pytest -q
```

Result:

```text
27 passed, 4 warnings in 0.26s
```

The warnings are existing Starlette/FastAPI deprecation warnings and do not indicate test failures.

Direct API contract checks using `TestClient`:

| Request | Expected | Actual |
|---|---|---|
| Create without `due_date` | `201`, `due_date: null` | Pass |
| Create with `due_date: "2026-08-15"` | `201`, same ISO date returned | Pass |
| Create with `due_date: "not-a-date"` | `422`, error located at `due_date` | Pass |
| PATCH with `due_date: null` | `200`, due date removed | Pass |

Live-server checks:

| URL/check | Result |
|---|---|
| `http://localhost:5500/` | `200 text/html` |
| `http://localhost:8000/health` | `200 application/json` |
| `http://localhost:8000/tasks` | `200 application/json` |
| `http://localhost:8000/openapi.json` | `200 application/json` |
| CORS origin `http://localhost:5500` | `Access-Control-Allow-Origin: http://localhost:5500` |

## Manual Browser Checks

A browser render was inspected with four controlled tasks on 2026-07-31.

| Check | Result | Evidence |
|---|---|---|
| Three Kanban columns remain visible | Pass | Browser showed To Do, In Progress, and Done with counts `2`, `1`, and `1` |
| Past-due active task is highlighted | Pass | ToDo task due 2026-07-30 had a red edge and `Overdue - Due Jul 30, 2026` |
| Task due today is not overdue | Pass | ToDo task due 2026-07-31 displayed its date without overdue styling |
| Completed past-due task is not overdue | Pass | Done task due 2026-07-29 displayed its date without overdue styling |
| Task without a due date has no date label | Pass | InProgress task rendered without misleading date text |
| Priority presentation remains visible | Pass | High, Medium, and Low priority badges rendered normally |

Completed browser interaction checks:

| Interaction | Result | Evidence |
|---|---|---|
| Toggle **Show overdue only** | Pass | Only `Overdue active` remained; column counts were `ToDo: 0`, `InProgress: 1`, and `Done: 0` |
| Open **New Task** | Pass | The due-date field opened with an empty value and `required=false` |
| Edit a dated task | Pass | Editing `Due today task` pre-filled the date as `2026-07-31` |
| Clear and save a due date | Pass | The PATCH succeeded, the board refreshed, and the task no longer contained a due-date element |
| Drag an overdue task through a valid transition to `Done` | Pass | The card moved from `InProgress` to `Done`, overdue styling was removed, and the API returned the task with status `Done` |

These interactions were executed in a real local Chromium browser against a controlled in-memory API instance on 2026-07-31. The browser used the actual form controls, submit handlers, fetch requests, and drag-and-drop events. The isolated API used port `8001` to avoid changing normal application data; the frontend API URL was restored to `http://localhost:8000` immediately after verification.

## Feature 1 Behavior Contract Before and After Implementation

| Behavior | Before | After |
|---|---|---|
| Task without a deadline | No date field | `due_date` is `null`; existing task creation remains valid |
| Task with a deadline | Rejected as an extra field | ISO date accepted and returned |
| Invalid deadline | Field did not exist | Invalid date rejected with `422` |
| Remove deadline | Not supported | PATCH with `due_date: null` removes it |
| Overdue calculation | Not available | Date before local today and status not `Done` |
| Due today | Not available | Not overdue |
| Completed task with past date | Not available | Date shown but not overdue |
| Overdue filtering | Not available | Filters the loaded task array before grouping |
| Empty filtered columns | Not applicable | Remain visible with count `0` |
| Priority sorting | High, Medium, Low, then ID | Unchanged |
| Status values | `ToDo`, `InProgress`, `Done` | Unchanged |
| API routes | Existing CRUD routes | Unchanged; no new filter endpoint |
| Frontend dependencies | Vanilla HTML/CSS/JavaScript | Unchanged; no dependency added |

## Break Test Evidence

Break Tests were controlled temporary mutations. Each mutation was restored immediately after the expected failure.

### Break Test 1: Due date is not persisted

Temporary mutation:

```python
due_date=None
```

instead of:

```python
due_date=payload.due_date
```

Command:

```powershell
.\venv\Scripts\python.exe -m pytest `
  test/test_tasks.py::test_create_task_with_due_date_returns_201 -q
```

Observed failure:

```text
AssertionError: assert None == '2026-08-15'
1 failed
```

Conclusion: the test detects a storage regression that silently drops a supplied due date.

### Break Test 2: Invalid dates are accepted

Temporary mutation: change create/response `due_date` types from `Optional[date]` to `Optional[str]`.

Command:

```powershell
.\venv\Scripts\python.exe -m pytest `
  test/test_tasks.py::test_create_task_invalid_due_date_returns_422 -q
```

Observed failure:

```text
assert 201 == 422
1 failed
```

Conclusion: the test detects weakened validation that allows malformed date strings.

### Restoration Check

Both temporary mutations were restored. The final full suite returned:

```text
27 passed
```

---

# Feature 2 Verification: Search and Combined Filters

**Verification date:** 2026-07-31  
**Backend feature commit:** `8caf433`  
**Frontend feature commit:** `e3543c1`

## Feature 2 Baseline Check

The Feature 2 baseline was inspected from the commit immediately before its backend commit.

| Check | Before Feature 2 | After Feature 2 |
|---|---:|---:|
| Pytest tests collected | 27 | 36 |
| Backend search parameter | Not present | `search` |
| Backend field filters | `status`, `priority` | `status`, `priority`, `assignee`, `due_date` |
| Combined-filter tests | 0 | 1 full AND-combination test |
| Feature 2 API tests | 0 | 9 |
| Frontend search/filter bar | Not present | Present above the board |

Baseline command:

```powershell
git show 8caf433^:test/test_tasks.py |
  Select-String -Pattern '^def test_' |
  Measure-Object
```

Result: `27` test functions. The baseline `GET /tasks` route had only status and priority filters, and the frontend had no Feature 2 filter bar.

## Feature 2 Backend Test Results

Full-suite command:

```powershell
.\venv\Scripts\python.exe -m pytest -q
```

Result:

```text
36 passed, 4 warnings in 0.48s
```

The warnings are existing Starlette/FastAPI deprecation warnings and do not indicate failures.

Direct API contract checks using `TestClient`:

| Request | Expected | Actual |
|---|---|---|
| `search=CHECKLIST` matching description text | `200`, one matching task | Pass |
| All five backend filters with one matching task | `200`, exactly one task | Pass |
| Search with no matches | `200`, `[]` | Pass |
| Invalid status `Blocked` | `422`, error located at `status` | Pass |
| Invalid priority `Urgent` | `422`, error located at `priority` | Pass |
| Invalid due date | `422`, error located at `due_date` | Pass |

Live OpenAPI contract:

```text
GET /tasks parameters:
search, status, priority, assignee, due_date
```

The schema contains no backend `overdue` parameter because overdue-only filtering remains client-side.

Live-server checks:

| URL/check | Result |
|---|---|
| `http://localhost:5500/` | `200 text/html` |
| `http://localhost:8000/health` | `200 application/json` |
| `GET /tasks?search=missing` | `200` with `[]` |
| Full combined-filter query | `200` |
| CORS origin `http://localhost:5500` | `Access-Control-Allow-Origin: http://localhost:5500` |

## Feature 2 Manual Browser Checks

A browser render was inspected at a 1600 by 1000 viewport.

| Check | Result | Evidence |
|---|---|---|
| Filter bar appears above the board | Pass | Search and field controls rendered between the header and board |
| All required controls are present | Pass | Search, status, priority, assignee, due date, Apply, and Clear were visible |
| Filter bar remains compact on a wide screen | Pass | Controls rendered in one aligned row |
| Three Kanban columns remain visible | Pass | To Do, In Progress, and Done were all rendered |
| Empty board behavior is preserved | Pass | Every column showed count `0` and its existing placeholder |
| Existing overdue-only control remains available | Pass | The header checkbox remained visible |

Completed browser interaction checks:

| Interaction | Result | Evidence |
|---|---|---|
| Search for description-only text | Pass | Searching `description-only-zebra` displayed only `No deadline task` |
| Apply status and priority together | Pass | `status=ToDo` and `priority=High` displayed only `Combined target` |
| Apply assignee and due date together | Pass | Only `Combined target` appeared, and the captured request was `/tasks?assignee=Sara&due_date=2026-08-15` |
| Apply filters with no matches | Pass | All three columns remained visible with counts `0`, three placeholders appeared, and the no-match message was shown |
| Click **Clear** | Pass | Search, field filters, and overdue-only reset; all six controlled tasks returned |
| Drag while a status filter is active | Pass | Moving `No deadline task` out of `InProgress` removed it after the filtered refresh while the status filter remained active |
| Create while an assignee filter is active | Pass | Creating `UI filter task` with assignee `UI Keeper` refreshed the board and preserved the `UI Keeper` filter |
| Edit while an assignee filter is active | Pass | Renaming the task to `UI filter task edited` refreshed the board and preserved the filter |

These checks used the same controlled local Chromium session described for Feature 1 and exercised the actual filter form, modal, network requests, board rendering, and drag-and-drop handlers.

## Feature 2 Behavior Contract Before and After Implementation

| Behavior | Before | After |
|---|---|---|
| Text search | Not supported | Case-insensitive partial search across title and description |
| Whitespace-only search | Not applicable | Treated as no search |
| Status filter | Supported | Preserved |
| Priority filter | Supported | Preserved |
| Assignee filter | Not supported | Case-insensitive exact match |
| Due-date filter | Not supported | Exact ISO date match |
| Invalid status or priority | `422` through enum validation | Preserved |
| Invalid due date | Not applicable | `422` through date validation |
| Multiple filters | Status and priority only | Search, status, priority, assignee, and due date use AND semantics |
| Valid no-match result | `200` with `[]` | Preserved for every combination |
| Backend overdue filter | Not supported | Still not supported; overdue-only remains client-side |
| Empty filtered columns | Visible | Preserved with count `0` and placeholders |
| Priority sorting | High, Medium, Low, then ID | Unchanged |
| Drag-and-drop | Supported | Preserved; active backend filters are reapplied after successful moves |
| Modal create/edit | Supported | Preserved; successful saves refresh with active filters |
| Loading, ready, empty, error | Supported | Preserved |
| Dependencies | Vanilla frontend and existing FastAPI stack | Unchanged |

## Focused Refactor Verification

The working Feature 2 checkpoint was committed before this refactor. On 2026-07-31, the full suite was run immediately before the change:

```text
36 passed, 4 warnings
```

The refactor was limited to `app/storage.py`. The inline combined-filter expression in `get_all_tasks()` was extracted into `_matches_task_filters()`. Search normalization, assignee normalization, filter parameters, AND semantics, response data, routes, and validation behavior were intentionally unchanged. No frontend file was modified.

Behavior contract:

| Behavior | Before refactor | After refactor |
|---|---|---|
| No filters | Return every task | Unchanged |
| Text search | Case-insensitive title/description partial match | Unchanged |
| Whitespace search | Behave like no search | Unchanged |
| Status and priority | Exact enum matches | Unchanged |
| Assignee | Case-insensitive exact match | Unchanged |
| Due date | Exact date match | Unchanged |
| Combined filters | Apply every active filter with AND semantics | Unchanged |
| Valid no-match query | Return `200` with `[]` | Unchanged |
| Invalid enum or date | Return `422` through FastAPI validation | Unchanged |
| Frontend behavior | Existing verified Kanban interactions | Unchanged; `frontend/index.html` had no diff |

Focused post-refactor command:

```powershell
.\venv\Scripts\python.exe -m pytest test/test_tasks.py -k "list_tasks" -q
```

Result:

```text
12 passed, 24 deselected, 1 warning
```

Full post-refactor command:

```powershell
.\venv\Scripts\python.exe -m pytest -q
```

Result:

```text
36 passed, 4 warnings
```

The identical full-suite result and passing list-task contract confirm that the refactor changed code organization without changing observable behavior.

## Feature 2 Break Test Evidence

Each Break Test used a controlled temporary mutation that was restored immediately after the expected failure.

### Feature 2 Break Test 1: Description search is removed

Temporary mutation: remove this condition from the storage search predicate:

```python
or normalized_search in task.description.casefold()
```

Command:

```powershell
.\venv\Scripts\python.exe -m pytest `
  test/test_tasks.py::test_list_tasks_searches_title_and_description_case_insensitively -q
```

Observed failure:

```text
AssertionError: returned task IDs did not include the description-only match
1 failed
```

Conclusion: the test detects a regression that limits search to titles.

### Feature 2 Break Test 2: Combined filters use OR

Temporary mutation: change the final due-date combination from:

```python
and (due_date is None or task.due_date == due_date)
```

to:

```python
or (due_date is None or task.due_date == due_date)
```

Command:

```powershell
.\venv\Scripts\python.exe -m pytest `
  test/test_tasks.py::test_list_tasks_combines_all_filters_with_and_behavior -q
```

Observed failure:

```text
AssertionError: response contained two extra tasks
1 failed
```

Conclusion: the test detects a regression from required AND semantics to overly broad OR behavior.

### Feature 2 Restoration Check

Both temporary mutations were restored. The final full suite returned:

```text
36 passed
```
