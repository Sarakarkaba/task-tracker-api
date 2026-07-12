from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from app.models import (
    TaskCreate,
    TaskPriority,
    TaskResponse,
    TaskStatus,
    TaskUpdate,
)


_tasks: dict[str, TaskResponse] = {}


def add_task(payload: TaskCreate) -> TaskResponse:
    now = datetime.now(timezone.utc)
    task = TaskResponse(
        id=str(uuid4()),
        title=payload.title,
        description=payload.description or "",
        status=payload.status,
        priority=payload.priority,
        assignee=payload.assignee,
        created_at=now,
        updated_at=now,
    )
    _tasks[task.id] = task
    return task


def get_all_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
) -> list[TaskResponse]:
    return [
        task
        for task in _tasks.values()
        if (status is None or task.status == status)
        and (priority is None or task.priority == priority)
    ]


def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    return _tasks.get(task_id)


def update_task(
    task_id: str,
    payload: TaskUpdate,
) -> Optional[TaskResponse]:
    current = _tasks.get(task_id)
    if current is None:
        return None

    updates = payload.model_dump(exclude_unset=True)
    if updates.get("description") is None and "description" in updates:
        updates["description"] = ""

    changed = any(getattr(current, key) != value for key, value in updates.items())
    if not changed:
        return current

    updates["updated_at"] = datetime.now(timezone.utc)
    updated = TaskResponse(
        **current.model_dump(exclude=set(updates)),
        **updates,
    )
    _tasks[task_id] = updated
    return updated


def delete_task(task_id: str) -> bool:
    return _tasks.pop(task_id, None) is not None


def _reset() -> None:
    _tasks.clear()
