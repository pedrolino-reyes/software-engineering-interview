"""
All of our e2e tests. There is some overlap with the integration tests, but we
just want to run some important tests to ensure the PostgreSQL database is
working as expected.
"""


def test_get_tasks(api):
    response = api.get("/tasks")
    assert response.status_code == 200

    # check that the response is a list of tasks
    assert isinstance(response.json(), list)
    # we've seeded the database and there should be at least 15 tasks in the
    # database, but only 10 should be returned by this endpoint
    assert len(response.json()) == 10


def test_create_and_get_task(api):
    payload = {
        "title": "Technical test",
        "description": "Do the python test for the QA position at Mitiga",
        "completed": False
    }
    response = api.post("/tasks", json=payload)
    assert response.status_code == 200
    assert response.json()["title"] == payload["title"]
    assert response.json()["description"] == payload["description"]
    assert response.json()["completed"] == payload["completed"]
    assert response.json()["id"] is not None

    # now get the newly created task by its ID
    task_id = response.json()["id"]
    assert isinstance(task_id, int)

    response = api.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == payload["title"]
    assert response.json()["description"] == payload["description"]
    assert response.json()["completed"] == payload["completed"]
    assert response.json()["id"] == task_id


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


def test_delete_task(api):
    # find a task to delete
    response = api.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) > 0
    task_id = response.json()[0]["id"]
    task_title = response.json()[0]["title"]

    # delete the task
    response = api.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == task_title

    # try to get the task again, we expect a 404
    response = api.get(f"/tasks/{task_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_create_update_and_delete_task(api):
    # create a task
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

    # try to get the task, we expect a 200
    response = api.get(f"/tasks/{task_id}")
    assert response.status_code == 200

    # update the task
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

    # delete the task
    response = api.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == payload["title"]

    # try to get the task again, we expect a 404
    response = api.get(f"/tasks/{task_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
