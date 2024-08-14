def test_get_and_update_task(api):
    response = api.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) > 0
    task_id = response.json()[0]["id"]

    response = api.get(f"/tasks/{task_id}")
    payload = {
      "title": "updated title",
      "description": "updated description",
      "completed": True
    }
    response = api.put(f"/tasks/{task_id}", json=payload)

    assert response.status_code == 200
    assert response.json()["title"] == payload["title"]
    assert response.json()["description"] == payload["description"]
    assert response.json()["completed"] == payload["completed"]


def test_get_and_delete_task(api):
    response = api.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) > 0
    task_id = response.json()[0]["id"]
    task_title = response.json()[0]["title"]

    response = api.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == task_title

    # now try to get the task again, it should return a 404
    response = api.get(f"/tasks/{task_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_create_update_and_delete_task(api):
    """
    This test creates a task, updates it, and then deletes it.
    """
    payload = {
        "title": "Pack briefcase",
        "description": "Pack suitcases for your holiday",
        "completed": False
    }
    response = api.post("/tasks", json=payload)
    assert response.status_code == 200
    assert response.json()["title"] == payload["title"]
    assert response.json()["description"] == payload["description"]
    assert response.json()["completed"] == payload["completed"]
    assert response.json()["id"] is not None

    task_id = response.json()["id"]

    # now update the task
    payload = {
        "title": "Pack suitcase",
        "description": "Pack suitcases for your trip to London",
        "completed": True
    }
    response = api.put(f"/tasks/{task_id}", json=payload)
    assert response.status_code == 200
    assert response.json()["title"] == payload["title"]
    assert response.json()["description"] == payload["description"]
    assert response.json()["completed"] == payload["completed"]

    # now delete the task
    response = api.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == payload["title"]

    # now try to get the task again, it should return a 404
    response = api.get(f"/tasks/{task_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

