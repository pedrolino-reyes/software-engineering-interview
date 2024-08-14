
def test_get_tasks(api):
    response = api.get("/tasks")
    assert response.status_code == 200

    # check that the response is a list of tasks
    assert type(response.json()) == list
    assert len(response.json()) > 0


def test_get_tasks_endpoint_returns_max_10_tasks(api):
    """
    Our database seed populates the database with 15 tasks. The /tasks endpoint should
    only return 10 of them.
    """
    response = api.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 10


def test_get_task_by_id(api):
    response = api.get("/tasks")
    assert response.status_code == 200
    assert type(response.json()) == list
    assert len(response.json()) > 0

    task = response.json()[0]
    task_id = response.json()[0]["id"]
    response = api.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id
    assert response.json()["title"] == task["title"]
    assert response.json()["description"] == task["description"]
    assert response.json()["completed"] is task["completed"]


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
    assert type(task_id) == int

    response = api.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == payload["title"]
    assert response.json()["description"] == payload["description"]
    assert response.json()["completed"] == payload["completed"]
    assert response.json()["id"] == task_id

