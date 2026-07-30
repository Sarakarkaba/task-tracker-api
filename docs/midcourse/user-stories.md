# FEATURE 1 : Due Dates and Overdue Filter
------------------------------------------

# Story 1: Assign a due date
As a user, I want to assign an optional due date when creating a task so that I know when it should be completed.
### Acceptance criteria
- The create modal includes an optional due-date field.
- A task can be created without a due date.
- A valid due date is saved and returned by the API.
- An invalid due-date value produces a validation error.
**Corrected AI assumption:** The AI initially treated a due date as required; the requirement was corrected so due dates are optional.

## Story 2: Update or remove a due date
As a user, I want to update or remove a task's due date so that its deadline remains accurate.
### Acceptance criteria
- The edit modal displays the task's current due date.
- Saving a different date updates the existing task.
- Submitting `due_date: null` removes the existing due date.
- Updating another field without including `due_date` preserves the current due date.
**Corrected AI assumption:** The AI initially assumed a cleared date should be saved as an empty string; the requirement was corrected so clearing the field removes the due date.

## Story 3: Display due dates on cards
As a user, I want to see due dates on task cards so that I can understand upcoming deadlines quickly.
### Acceptance criteria
- A card with a due date displays it in a readable format.
- A card without a due date does not display misleading date text.
- Displaying due dates does not change priority sorting.
**Corrected AI assumption:** The AI initially assumed every card should display a "No due date" label; the requirement was corrected so cards without due dates omit the date text.

## Story 4: Highlight overdue tasks
As a user, I want overdue tasks to be visually highlighted so that missed deadlines are easy to identify.
### Acceptance criteria
- A task is overdue when its due date is earlier than today and its status is not 'Done'.
- Overdue calculation compares the due date with the backend server's current calendar date.
- Overdue cards have a clear visual indicator.
- Completed tasks are not marked overdue.
- Tasks due today are not marked overdue.
- Cards without due dates are not marked overdue.
**Corrected AI assumption:** The AI initially treated every task with a past due date as overdue; the requirement was corrected to exclude completed tasks.

## Story 5: Filter overdue tasks
As a user, I want to filter the board to show only overdue tasks so that I can focus on missed deadlines.
### Acceptance criteria
- The frontend provides an overdue-only filter control.
- Overdue filtering is applied in the browser to the tasks returned by `GET /tasks`; the backend does not accept an `overdue` query parameter.
- When the control is active, only tasks whose due date is earlier than the browser's local calendar date and whose status is not `Done` are displayed.
- Tasks due today are not displayed as overdue.
- Tasks without a due date are not displayed as overdue.
- Completed tasks are not displayed as overdue even when their due date is in the past.
- When no overdue tasks match, all three columns remain visible with count `0` and their empty-state placeholders.
- Applying the overdue filter keeps all three Kanban columns visible and preserves their empty states.
**Corrected AI assumption:** The AI initially proposed an `overdue=true` backend filter; the requirement was corrected so overdue filtering remains a small, client-side feature.



# FEATURE 2 : Search and Combined filters
-----------------------------------------

# Story 1: Search task text
As a user, I want to search task titles and descriptions so that I can find relevant work quickly.
### Acceptance criteria
- `GET /tasks` accepts an optional text-search query.
- Search checks both `title` and `description`.
- Search is case-insensitive.
- Partial matches are included.
- No matches return `200` with `[]`.
- An empty or whitespace-only search behaves like no search.
**Corrected AI assumption:** The AI initially included IDs and assignee names in text search; the requirement was corrected so text search checks only titles and descriptions.

## Story 2: Filter by task fields
As a user, I want to filter tasks by status, priority, or assignee so that I can focus on a specific subset of work.
### Acceptance criteria
- Status accepts only `ToDo`, `InProgress`, or `Done`.
- Priority accepts only `Low`, `Medium`, or `High`.
- Assignee filtering returns tasks assigned to the requested person.
- An invalid status or priority returns `422`.
- Omitting filters preserves the existing `GET /tasks` behavior.

## Story 3: Filter by due date
As a user, I want to filter tasks by due date so that I can focus on work due on a specific day.
### Acceptance criteria
- `GET /tasks` accepts an optional ISO due date in `YYYY-MM-DD` format.
- Only tasks with that exact due date are returned.
- Tasks without due dates do not match a due-date filter.
- An invalid due date returns `422`.

## Story 4: Combine search and filters
As a user, I want to combine text search with multiple filters so that I can narrow the board precisely.

### Acceptance criteria
- Search, status, priority, assignee, and due date can be supplied together.
- Combined filters use AND behavior.
- Every returned task satisfies every active filter.
- A valid combination with no matches returns `200` with `[]`.
