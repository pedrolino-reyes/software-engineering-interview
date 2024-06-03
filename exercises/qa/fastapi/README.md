# QA - FastAPI Exercise

## Goal

The goal of providing an exercise is to evaluate the candidate's ability to solve real-world problems and demonstrate their technical skills in action.

The candidate will be required to defend their solution in the interview, justifying why they have made certain decisions to implement and test the API.

## Description

Develop a small API to manage a to-do list. The API should allow the following operations:

- Create a task.
- Get a task by its ID.
- Get all tasks.
- Update a task by its ID.
- Delete a task by its ID.

Each task should have the following fields:

- **ID** (auto-generated, integer).
- **Title** (string).
- **Description** (string).
- **Status** (boolean, default is False).

When creating the task the following validations must be applied:

- Title length validation: The task title must be between 5 and 50 characters.
- Description length validation: The task description must be at least 10 characters.

## Requirements

- Implement the API using FastAPI and PostgreSQL as storage system.
- Use Poetry as a dependency management system.
- Validate the input data using Pydantic.
- Make appropriate use of HTTP status codes (200, 400, 404...) in endpoint responses.
- Write unit tests that do not depend on infrastructure services like the database, instead use mocks.
  - What parts of the application would you unit test? The number of tests is not as relevant as the components that are tested.
- Write integration tests that use a PostgreSQL database running in Docker instead of using mocks. Tip: docker-compose can be used to do so easily.
  - What parts of the application would you unit test? The number of tests is not as relevant as the components that are tested.
- Write a load test on one of the implemented endpoints. Tip: [Locust](https://locust.io) or [K6](https://k6.io) can used to do so easily.
  - If you can, attach a screenshot of the test report to see the endpoint response time curve as the test increases or decreases the load.
- How would you apply regression testing in this project?
- If it were up to you, what stages would the life cycle of this application include to ensure a high quality standard?
- Regarding testing, where does a unit and integration test begin and end? That is, what are their differences?
- How can you measure the code quality of this project? What metrics/characteristics make up quality?
