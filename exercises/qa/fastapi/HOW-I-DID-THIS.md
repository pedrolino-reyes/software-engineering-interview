# How I went about the technical challenge

I thought I'd include a file to explain how I worked through this technical challenge, with some notes to explain the decisions that were made.

I worked through this challenge in the following order.

1. e2e tests
1. integration tests
1. unit tests

## e2e tests

I made the decision to control the database with these tests and added a fixture that initialised the database in a known state and then truncated all the data at the end of the test run. I did this to simplify some of the tests. It's not always possible to do this in e2e tests, where you might not have control of the database being used on a test server for example, but it was possible here so I went ahead...

In writing the e2e tests, I uncovered an issue: the update endpoint didn't update the task description at all. The other fields were updated correctly. I fixed the app code when I discovered this bug.

I started with a lot of e2e tests, and when it came to implementing integration tests, I saw that I could move quite a few of them into the integration pack, since the in-memory database would be sufficient to test the functionality.

## Integration tests

This is a fairly simple app, and most of the important functionality is provided by FastAPI and SQL Alchemy, which are used to define the RESTful API and manage the database. There's no need to unit test these libraries - they aren't our product. But we want to make sure we've got everything configured and working together properly.

Given that SQL Alchemy is designed for different databases, it's possible to just swap out PostgreSQL for an in-memory database, and run integration tests quickly and reliably in memory. This is what I did here. The bulk of the tests we have are integration tests.

## Unit tests

Typically, unit tests should focus on "business logic" or, in our case, application logic that doesn't involve calls to the database. There aren't many unit tests - I kept them focused on the small amount of logic in the `crud.py` file that doesn't relate to database persistence. The rest of the app was a better candidate for integration tests.

The db persistence is tested properly by the integration and e2e tests, and the unit tests just assert that the expected db methods are called. Even this could be considered overkill - there's no real need, and it does arguably make the unit tests more brittle. The integration tests will pick up on any errors with the calls to the persistence layer. But I left the code there just to provide another example on how we can spy on mock objects. For this reason, there are no unit tests for `get_task`, `get_tasks` or `update_task`: these functions really just make database calls, with no other logic to test, and they're tested sufficiently by the integration tests.

## Test coverage

The coverage report shows that only the real database connection (`app/database.py`) isn't covered by the unit and integration tests. It's possible to add a `.coveragerc` file to automatically exclude this file from the coverage report, in the case that we want to enforce 100% test coverage.




- Write a load test on one of the implemented endpoints. Tip: [Locust](https://locust.io) or [K6](https://k6.io) can used to do so easily.
  - If you can, attach a screenshot of the test report to see the endpoint response time curve as the test increases or decreases the load.
- How would you apply regression testing in this project?
- If it were up to you, what stages would the life cycle of this application include to ensure a high quality standard?
- Regarding testing, where does a unit and integration test begin and end? That is, what are their differences?
- How can you measure the code quality of this project? What metrics/characteristics make up quality?


## Additional python libraries

I installed the following libraries using poetry (this is reflected in the change to pyproject.toml):

- pytest
- pytest-cov
- pytest-mock
- requests


# Other things I did

I moved the .gitignore file to the root of the repo. I'd opened files on a Mac, which had added .DS_Store files at levels above the `fastapi` folder, and I wanted to ignore them all.

I use