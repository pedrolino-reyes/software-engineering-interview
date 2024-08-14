
def test_get_tasks(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert type(response.json()) == list


def test_create_and_get_task(client):
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

    # now get the newly created task by its ID
    task_id = response.json()["id"]
    assert type(task_id) == int

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == payload["title"]
    assert response.json()["description"] == payload["description"]
    assert response.json()["completed"] == payload["completed"]
    assert response.json()["id"] == task_id

    # and get all the tasks to verify the new task is there
    response = client.get("/tasks")
    assert response.status_code == 200
    assert type(response.json()) == list
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == task_id
    assert response.json()[0]["title"] == payload["title"]
    assert response.json()[0]["description"] == payload["description"]
    assert response.json()[0]["completed"] == payload["completed"]
