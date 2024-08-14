# QA - FastAPI Exercise

## Goal

The goal of providing an exercise is to evaluate the candidate's ability to solve real-world problems and demonstrate their technical skills in action.

The candidate will be required to defend their solution in the interview, justifying why they have made certain decisions to test the API.

## Description

Test a small API to manage a to-do list. The API has the following operations:

- Create a task.
- Get a task by its ID.
- Get all tasks.
- Update a task by its ID.
- Delete a task by its ID.

Each task has the following fields:

- **ID** (auto-generated, integer).
- **Title** (string).
- **Description** (string).
- **Status** (boolean, default is False).

When creating the task the following validations are applied:

- Title length validation: The task title must be between 5 and 50 characters.
- Description length validation: The task description must be at least 10 characters.

## Requirements

- Write unit tests that do not depend on infrastructure services like the database, instead use mocks.
  - What parts of the application would you unit test? The number of tests is not as relevant as the components that are tested.
- Write integration tests that use a PostgreSQL database running in Docker instead of using mocks. Tip: docker-compose can be used to do so easily.
  - What parts of the application would you unit test? The number of tests is not as relevant as the components that are tested.
- Add content to the section [6. Running tests with Poetry](#6-running-tests-with-poetry) to explain how to run the tests and generate coverage reports.
- Write a load test on one of the implemented endpoints. Tip: [Locust](https://locust.io) or [K6](https://k6.io) can used to do so easily.
  - If you can, attach a screenshot of the test report to see the endpoint response time curve as the test increases or decreases the load.
- How would you apply regression testing in this project?
- If it were up to you, what stages would the life cycle of this application include to ensure a high quality standard?
- Regarding testing, where does a unit and integration test begin and end? That is, what are their differences?
- How can you measure the code quality of this project? What metrics/characteristics make up quality?

### To watch out

The application code may present some intentional error to provide greater richness and complexity to the exercise.

## Project Structure

The basic structure of the project could be something like this or similar (not strictly the same):

```
fastapi/
├── app/
│   ├── __init__.py
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
└── tests/
│   ├── __init__.py
│   ├── test_integration.py
│   ├── test_unit.py
└── docker-compose.yaml
└── poetry.lock
└── pyproject.toml
└── README.md
```

## Initializing the project

### 1. Initialize Your Project with Poetry

```
poetry init
```

### 2. Add Dependencies

```
poetry add fastapi sqlalchemy pydantic psycopg2-binary
poetry add --dev pytest pytest-asyncio httpx
```

### 3. Check Virtual Environment

Poetry automatically creates a virtual environment for your project. You can check where Poetry has created the virtual environment with:

```
poetry env info
```

### 4. Activate the Virtual Environment

If you need to activate the virtual environment manually (for example, to run a command in it), you can do so with:

```
poetry shell
```

### 5. Running API with Poetry

Execute the following Docker command to get up and running the PostgreSQL database.

```
docker-compose up -d
```

Execute the following Poetry command to get up a server and run the API.

```
poetry run uvicorn app.main:app --reload
```

### 6. Running tests with Poetry

There are 3 sets of tests:

1. Unit tests
2. Integration tests
3. End to end (e2e) tests

pytest is used to run all three types of test.

#### Unit tests
The unit tests run in-memory and are extremely fast as a result. They test the code logic and don't involve writing to disk or to the database.

Ideally, unit tests will cover as much code as possible. This makes them a valuable resource when it comes to refactoring code - they will alert us instantly if any logic is broken inadvertently. For this reason, it is a good idea to run a code coverage report when running the unit tests.

```
poetry run pytest tests/unit
```

#### Integration tests
The integration tests require an instance of PostgreSQL to be running. You'll need to start the docker container before running these tests, as they test the integration of our app with PostgreSQL and make sure we are using the database as intended.

```
poetry run pytest tests/integration
```

#### Measuring code coverage

The unit and integration tests are run in the same process as the code they test, so meaningful code coverage reports can be created. You can get a quick summary of coverage in the terminal with the `--cov-report term` option.

To run code coverage for just the unit tests:

```
poetry run pytest tests/unit --cov-report term --cov=app
```

To run code coverage for just the integration tests:

```
poetry run pytest tests/integration --cov-report term --cov=app
```

The unit and integration tests can be run together to get a view on how much of the application code is covered by tests:

```
poetry run pytest tests/unit tests-integration --cov-report term --cov=app
```


You can run a code coverage report for the e2e tests, but you won't get anything useful. The e2e tests run against an app running in a separate process, and the coverage tool can't track which lines of code are being executed.

#### E2E tests
To run the e2e tests, you need to have first started the FastAPI server. The e2e tests test the endpoints of the Fast API server.

```
poetry run pytest tests/e2e
```

