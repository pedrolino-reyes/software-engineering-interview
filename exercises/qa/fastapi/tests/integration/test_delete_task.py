def test_create_and_delete_task(client):
    payload = {
        "title": "Task to delete",
        "description": "We'll create this, then delete it immediately",
        "completed": False
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 200
    assert response.json()["title"] == payload["title"]
    assert response.json()["description"] == payload["description"]
    assert response.json()["completed"] == payload["completed"]
    assert response.json()["id"] is not None

    # now get the newly created task by its ID
    task_id = response.json()["id"]
    assert type(task_id) == int

    response = client.delete(f"/tasks/{task_id}")
    import pytest; pytest.set_trace()
    assert response.status_code == 200

    # try to get the task again, we expect a 404
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404

def test_delete_task_unsuccessful(client):
    response = client.delete("/tasks/9999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"