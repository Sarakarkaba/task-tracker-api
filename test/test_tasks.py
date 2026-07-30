def test_create_task_valid_returns_201_with_full_body(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Write tests",
            "description": "Cover the task API",
            "status": "ToDo",
            "priority": "High",
            "assignee": "Sara",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["id"]
    assert body["title"] == "Write tests"
    assert body["description"] == "Cover the task API"
    assert body["status"] == "ToDo"
    assert body["priority"] == "High"
    assert body["assignee"] == "Sara"
    assert body["due_date"] is None
    assert body["created_at"]
    assert body["updated_at"]


def test_create_task_with_due_date_returns_201(client):
    response = client.post(
        "/tasks",
        json={"title": "Prepare release", "due_date": "2026-08-15"},
    )

    assert response.status_code == 201
    assert response.json()["due_date"] == "2026-08-15"


def test_create_task_invalid_due_date_returns_422(client):
    response = client.post(
        "/tasks",
        json={"title": "Invalid deadline", "due_date": "not-a-date"},
    )

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert detail[0]["loc"][-1] == "due_date"


def test_create_task_missing_title_returns_422(client):
    response = client.post("/tasks", json={"priority": "Low"})
    assert response.status_code == 422


def test_create_task_blank_title_returns_422(client):
    response = client.post("/tasks", json={"title": "   "})
    assert response.status_code == 422


def test_create_task_invalid_priority_returns_422(client):
    response = client.post(
        "/tasks", json={"title": "Invalid priority", "priority": "Urgent"}
    )
    assert response.status_code == 422


def test_create_task_unknown_field_returns_422(client):
    response = client.post(
        "/tasks", json={"title": "Unknown field", "unexpected": True}
    )
    assert response.status_code == 422


def test_list_tasks_empty_returns_200_and_empty_list(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_status_no_match_returns_200_and_empty_list(
    client, created_task
):
    response = client.get("/tasks", params={"status": "Done"})
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_priority_returns_only_matches(client):
    low_response = client.post(
        "/tasks", json={"title": "Low priority task", "priority": "Low"}
    )
    high_response = client.post(
        "/tasks", json={"title": "High priority task", "priority": "High"}
    )
    assert low_response.status_code == 201
    assert high_response.status_code == 201

    response = client.get("/tasks", params={"priority": "High"})

    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == high_response.json()["id"]
    assert tasks[0]["priority"] == "High"


def test_get_task_by_id_returns_task(client, created_task):
    response = client.get(f"/tasks/{created_task['id']}")
    assert response.status_code == 200
    assert response.json() == created_task


def test_get_task_by_id_not_found_returns_404_with_detail(client):
    response = client.get("/tasks/missing-id")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task with id missing-id not found"}


def test_patch_partial_update_keeps_other_fields(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}", json={"title": "updated title"}
    )

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "updated title"
    assert body["description"] == created_task["description"]
    assert body["status"] == created_task["status"]
    assert body["priority"] == created_task["priority"]
    assert body["assignee"] == created_task["assignee"]
    assert body["created_at"] == created_task["created_at"]


def test_patch_due_date_updates_task(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"due_date": "2026-09-01"},
    )

    assert response.status_code == 200
    assert response.json()["due_date"] == "2026-09-01"
    assert response.json()["title"] == created_task["title"]


def test_patch_null_due_date_removes_task_due_date(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Task with deadline", "due_date": "2026-09-01"},
    )
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"due_date": None},
    )

    assert response.status_code == 200
    assert response.json()["due_date"] is None


def test_patch_not_found_returns_404(client):
    response = client.patch("/tasks/missing-id", json={"title": "updated title"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Task with id missing-id not found"}


def test_patch_valid_transition_todo_to_inprogress_returns_200(
    client, created_task
):
    response = client.patch(
        f"/tasks/{created_task['id']}", json={"status": "InProgress"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "InProgress"


def test_patch_valid_transition_inprogress_to_done_returns_200(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Complete drag-and-drop", "status": "InProgress"},
    )
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"status": "Done"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "Done"


def test_patch_valid_transition_done_to_inprogress_returns_200(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Reopen completed task", "status": "Done"},
    )
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"status": "InProgress"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "InProgress"


def test_patch_invalid_transition_todo_to_done_returns_422(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}", json={"status": "Done"}
    )
    assert response.status_code == 422
    assert response.json()["detail"].startswith(
        "Invalid status transition from ToDo to Done."
    )


def test_patch_invalid_transition_inprogress_to_todo_returns_422(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Keep task moving forward", "status": "InProgress"},
    )
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"status": "ToDo"},
    )

    assert response.status_code == 422
    assert response.json()["detail"].startswith(
        "Invalid status transition from InProgress to ToDo."
    )


def test_patch_same_status_returns_422(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}", json={"status": "ToDo"}
    )
    assert response.status_code == 422
    assert response.json()["detail"].startswith(
        "Invalid status transition from ToDo to ToDo."
    )


def test_patch_blank_title_returns_422(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"title": "   "},
    )

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert detail[0]["loc"][-1] == "title"
    assert "title must not be blank" in detail[0]["msg"]


def test_patch_invalid_priority_returns_422(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"priority": "Urgent"},
    )

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert detail[0]["loc"][-1] == "priority"
    assert "Low" in detail[0]["msg"]
    assert "Medium" in detail[0]["msg"]
    assert "High" in detail[0]["msg"]


def test_patch_missing_body_returns_422(client, created_task):
    response = client.patch(f"/tasks/{created_task['id']}")

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert detail[0]["loc"] == ["body"]
    assert "required" in detail[0]["msg"].lower()


def test_delete_existing_returns_204_no_body(client, created_task):
    response = client.delete(f"/tasks/{created_task['id']}")
    assert response.status_code == 204
    assert response.content == b""


def test_delete_missing_returns_404(client):
    response = client.delete("/tasks/missing-id")
    assert response.status_code == 404
