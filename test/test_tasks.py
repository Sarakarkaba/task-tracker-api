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
    assert body["created_at"]
    assert body["updated_at"]


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


def test_patch_invalid_transition_todo_to_done_returns_422(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}", json={"status": "Done"}
    )
    assert response.status_code == 422
    assert response.json()["detail"].startswith(
        "Invalid status transition from ToDo to Done."
    )


def test_patch_same_status_returns_422(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}", json={"status": "ToDo"}
    )
    assert response.status_code == 422
    assert response.json()["detail"].startswith(
        "Invalid status transition from ToDo to ToDo."
    )


def test_delete_existing_returns_204_no_body(client, created_task):
    response = client.delete(f"/tasks/{created_task['id']}")
    assert response.status_code == 204
    assert response.content == b""


def test_delete_missing_returns_404(client):
    response = client.delete("/tasks/missing-id")
    assert response.status_code == 404
