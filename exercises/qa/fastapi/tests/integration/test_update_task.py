def test_update_task_not_found(client):
    payload = {
        "title": "Failed update",
        "description": "Can't update a task that doesn't exist",
        "completed": False
    }
    response = client.put("/tasks/999999", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_create_and_update_task(client):
    payload = {
        "title": "Technical test",
        "description": "Do the python test for the QA position at Mitiga",
        "completed": False
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 200
    assert response.json()["title"] == payload["title"]
    assert response.json()["description"] == payload["description"]
    assert response.json()["completed"] == payload["completed"]
    assert response.json()["id"] is not None

    task_id = response.json()["id"]

    # update the task
    payload = {
        "title": "Successfule update",
        "description": "This task has been updated successfully",
        "completed": True
    }
    response = client.put(f"/tasks/{task_id}", json=payload)
    assert response.status_code == 200
    assert response.json()["title"] == payload["title"]
    assert response.json()["description"] == payload["description"]
    assert response.json()["completed"] == payload["completed"]
    assert response.json()["id"] == task_id
