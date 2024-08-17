"""
Tests relating to non-persistence logic of the functions in crud.py
(the persistence is handled by sqlalchemy and is tested in the integration tests).
"""

from unittest.mock import patch

import pytest

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.crud import create_task

# rather than repeating these messages in the app code and tests,
# it would be nice to move them to a shared location
VALID_DESCRIPTION = "This is a valid description"
VALID_TITLE = "This is a valid title"

TITLE_ERROR_MSG = "Title length must be between 5 and 50 characters"
DESCRIPTION_ERROR_MSG = "Description length must be at least 10 characters"


def task_create_side_effect(*args, **kwargs):
    """
    Side effect for the Task model creation. We're mocking the Task model,
    and we just return a stub message for our assertions.
    """
    return "task was created"


# Tests focusing on the title field.
def test_title_too_short(mocker):
    """
    Title must be at least 5 characters long.
    """
    db = mocker.MagicMock(Session)
    task = mocker.MagicMock(schemas.TaskCreate)
    task.title = "a" * 4

    with pytest.raises(HTTPException) as excinfo:
        create_task(db, task)

    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == TITLE_ERROR_MSG


@patch('app.models.Task')
def test_title_too_long(_Task, mocker):
    """
    Title must be at most 50 characters long.
    """
    db = mocker.MagicMock(Session)

    _Task.side_effect = task_create_side_effect

    # no error should be thrown with 50 characters
    task = mocker.MagicMock(schemas.TaskCreate)
    task.title = "a" * 50
    task.description = VALID_DESCRIPTION
    task.completed = False

    result = create_task(db, task)

    # this call passed validation, so the task object should be created and committed
    _Task.assert_called_with(
        title=task.title,
        description=task.description,
        completed=task.completed
    )

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()

    assert result == "task was created"

    # error should be thrown with 51 characters
    task = mocker.MagicMock(schemas.TaskCreate)
    task.title = "a" * 51

    with pytest.raises(HTTPException) as excinfo:
        create_task(db, task)

    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == TITLE_ERROR_MSG


@patch('app.models.Task')
def test_description_too_short(_Task, mocker):
    db = mocker.MagicMock(Session)

    # an error should be thrown with 9 characters
    task = mocker.MagicMock(schemas.TaskCreate)
    task.title = VALID_TITLE
    task.description = "a" * 9

    with pytest.raises(HTTPException) as excinfo:
        create_task(db, task)

    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == DESCRIPTION_ERROR_MSG

    # no error should be thrown with 10 characters
    task = mocker.MagicMock(schemas.TaskCreate)
    task.title = VALID_TITLE
    task.description = "a" * 10
    task.completed = False

    _Task.side_effect = task_create_side_effect

    result = create_task(db, task)

    # this call passed validation, so the task object should be created and committed
    _Task.assert_called_with(
        title=task.title,
        description=task.description,
        completed=task.completed
    )

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()

    assert result == "task was created"
