"""
Tests relating to the details of the create task endpoint.
"""

"""
Tests focusing on the title field.
"""

def test_title_is_required(api):
    """
    Title is a required field.
    """
    payload = {
        "description": "This is a valid description"
    }
    response = api.post("/tasks", json=payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Field required"
    assert response.json()["detail"][0]["type"] == "missing"


def test_title_too_short(api):
    """
    Title must be at least 5 characters long.
    """
    payload = {
        "title": "a" * 4,
        "description": "This is a valid description"
    }
    response = api.post("/tasks", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Title length must be between 5 and 50 characters"


def test_title_too_long(api):
    """
    Title must be at most 50 characters long.
    """
    payload = {
        "title": "a" * 51,
        "description": "This is a valid description"
    }
    response = api.post("/tasks", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Title length must be between 5 and 50 characters"


"""
Tests focusing on the description field.
"""
def test_description_is_required(api):
    """
    Description is a required field.
    """
    payload = {
        "title": "This is a valid title"
    }
    response = api.post("/tasks", json=payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Field required"
    assert response.json()["detail"][0]["type"] == "missing"


def test_unicode_handling(api):
    """
    Tests we can encode unicode characters from German correctly.

    (The desciption means: "Wrongful practicing of xylophone music tortures every larger dwarf")
    """
    payload = {
        "title": "German unicode test",
        "description": "Falsches Üben von Xylophonmusik quält jeden größeren Zwerg"
    }
    response = api.post("/tasks", json=payload)
    assert response.status_code == 200
    assert response.json()["title"] == payload["title"]
    assert response.json()["description"] == payload["description"]
    assert response.json()["completed"] == False

    # get the created task to verify it was stored correctly
    task_id = response.json()["id"]
    response = api.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == payload["title"]
    assert response.json()["description"] == payload["description"]
    assert response.json()["completed"] == False


def test_description_too_short(api):
    """
    Description must be at least 10 characters long.
    """
    payload = {
        "title": "Valid title",
        "description": "a" * 9
    }
    response = api.post("/tasks", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Description length must be at least 10 characters"


def test_description_can_be_really_long(api):
    payload = {
        "title": "Valid title",
        "description": "a" * 50000
    }
    response = api.post("/tasks", json=payload)
    assert response.status_code == 200
    assert response.json()["description"] == payload["description"]


"""
Tests focusing on the completed field.
"""
def test_completed_defaults_to_false(api):
    """
    When a task is created, the completed field should default to False.
    """
    payload = {
        "title": "Valid title",
        "description": "Valid description"
    }
    response = api.post("/tasks", json=payload)
    assert response.status_code == 200
    assert response.json()["completed"] == False


def test_completed_is_boolean_only(api):
    """
    Completed field must be a boolean.
    """
    payload = {
        "title": "Valid title",
        "description": "Valid description",
        "completed": "not a boolean"
    }
    response = api.post("/tasks", json=payload)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid boolean, unable to interpret input"
    assert response.json()["detail"][0]["type"] == "bool_parsing"