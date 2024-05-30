# FastAPI Exercise

## Goal

The goal of providing an exercise is to evaluate the candidate's ability to solve real-world problems and demonstrate their technical skills in action.

The candidate will be required to defend their solution in the interview, justifying why they have made certain decisions to implement the API.

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
- Write integration tests that use a PostgreSQL database running in Docker instead of using mocks. Tip: docker-compose can be used to do so easily.
