from datetime import date, datetime, timezone

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app import storage
from app.business_rules import validate_status_transition
from app.models import TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskUpdate


load_dotenv()


app = FastAPI(
    title="Module 1 Task Tracker API",
    description="A minimal FastAPI REST API for a learning-project task tracker.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],
    allow_methods=["GET", "POST", "PATCH"],
    allow_headers=["Content-Type"],
)


@app.get("/health")
def health_check():
    """Report the current health of the API.

    Returns:
        A mapping containing an ``ok`` status and the current UTC timestamp.

    Examples:
        Request:

        ``GET /health``
    """
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["tasks"],
)
def create_task(payload: TaskCreate) -> TaskResponse:
    """Create and store a task.

    Args:
        payload: The validated fields for the new task.

    Returns:
        The stored task, including its generated ID and timestamps.

    Examples:
        Request:

        ``POST /tasks``

        Body: ``{"title": "Write documentation", "priority": "High"}``
    """
    return storage.add_task(payload)


@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks(
    search: str | None = None,
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    assignee: str | None = None,
    due_date: date | None = None,
) -> list[TaskResponse]:
    """List tasks that match the supplied filters.

    Args:
        search: Optional case-insensitive text to find in titles or descriptions.
        status: Optional exact task status.
        priority: Optional exact task priority.
        assignee: Optional case-insensitive exact assignee name.
        due_date: Optional exact due date.

    Returns:
        All stored tasks that match every supplied filter.

    Examples:
        Request:

        ``GET /tasks?status=ToDo&priority=High``

        Search request:

        ``GET /tasks?search=documentation``
    """
    return storage.get_all_tasks(
        search=search,
        status=status,
        priority=priority,
        assignee=assignee,
        due_date=due_date,
    )


@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def get_task(task_id: str) -> TaskResponse:
    """Retrieve a task by ID.

    Args:
        task_id: The generated ID of the requested task.

    Returns:
        The matching task.

    Raises:
        HTTPException: If no task has the supplied ID.

    Examples:
        Request:

        ``GET /tasks/550e8400-e29b-41d4-a716-446655440000``
    """
    task = storage.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )
    return task


@app.patch("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
    """Update fields on an existing task.

    Args:
        task_id: The generated ID of the task to update.
        payload: The validated fields to replace.

    Returns:
        The updated task, or the existing task when no values changed.

    Raises:
        HTTPException: If no task has the supplied ID, or if the requested
            status transition is invalid.

    Examples:
        Request:

        ``PATCH /tasks/550e8400-e29b-41d4-a716-446655440000``

        Body: ``{"status": "InProgress"}``
    """
    if payload.status is not None:
        existing = storage.get_task_by_id(task_id)
        if existing is None:
            raise HTTPException(
                status_code=404,
                detail=f"Task with id {task_id} not found",
            )
        validate_status_transition(existing.status, payload.status)

    task = storage.update_task(task_id, payload)
    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )
    return task


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["tasks"],
)
def delete_task(task_id: str) -> None:
    """Delete a task by ID.

    Args:
        task_id: The generated ID of the task to delete.

    Returns:
        None.

    Raises:
        HTTPException: If no task has the supplied ID.

    Examples:
        Request:

        ``DELETE /tasks/550e8400-e29b-41d4-a716-446655440000``
    """
    if not storage.delete_task(task_id):
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )
