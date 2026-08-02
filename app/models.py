from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


class TaskStatus(str, Enum):
    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    description: Optional[str] = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None
    due_date: Optional[date] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        """Normalize and validate a new task title.

        Args:
            value: The title supplied for the new task.

        Returns:
            The title with leading and trailing whitespace removed.

        Raises:
            ValueError: If the stripped title is empty or longer than 200
                characters.
        """
        value = value.strip()
        if not value:
            raise ValueError("title must not be blank")
        if len(value) > 200:
            raise ValueError("title must not exceed 200 characters")
        return value


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None
    due_date: Optional[date] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: Optional[str]) -> Optional[str]:
        """Normalize and validate an updated task title.

        Args:
            value: The replacement title, or ``None`` when no title is
                supplied.

        Returns:
            The stripped title, or ``None`` when the input is ``None``.

        Raises:
            ValueError: If a supplied title is blank after stripping or longer
                than 200 characters.
        """
        if value is None:
            return None

        value = value.strip()
        if not value:
            raise ValueError("title must not be blank")
        if len(value) > 200:
            raise ValueError("title must not exceed 200 characters")
        return value


class TaskResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    assignee: Optional[str]
    due_date: Optional[date]
    created_at: datetime
    updated_at: datetime
