# How I went about the technical challenge, plus answers to some of the questions in the readme

Here I try to answer the questions in your readme, and explain some of the technical decisions that were made when implementing tests.

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

The coverage report shows that only the "real" database connection (`app/database.py`) isn't covered by the unit and integration tests. It's possible to add a `.coveragerc` file to automatically exclude this file from the coverage report, in the case that we want to enforce 100% test coverage.




- Write a load test on one of the implemented endpoints. Tip: [Locust](https://locust.io) or [K6](https://k6.io) can used to do so easily.
  - If you can, attach a screenshot of the test report to see the endpoint response time curve as the test increases or decreases the load.



## Additional python libraries

I installed the following libraries using poetry (this is reflected in the change to pyproject.toml):

- locust
- pytest
- pytest-cov
- pytest-mock
- requests


## Other things I did

I moved the .gitignore file to the root of the repo. I'd opened files on a Mac, which had added .DS_Store files at levels above the `fastapi` folder, and I wanted to ignore them all.

## Assessment questions

The readme had some additional questions. Here are my answers.

### How would you apply regression testing in this project?

Regression testing validates that new iterations of an app maintain all the required functionality that already existed. Automated tests are an excellent way to protect against regressions, since they document how the system worked at a given point in time. By running tests against new iterations, any unintended changes in existing behaviour ("regressions") will be caught automatically.

In this sense, automated tests can be very valuable, and arguably outshine manual testing in the case of large systems. It's far more time-consuming for a manual tester to go through all of the app's functionality every time a new release candidate is produced than it is for a computer to run existing test scripts.

### If it were up to you, what stages would the life cycle of this application include to ensure a high quality standard?

I would like to see the following stages, checks and ways of working:

1. Requirements communication using BDD approaches. The idea of "specification by example", for instance, can help teams communicate requirements effectively by identifying key examples that are communicated clearly in a codified manner. The idea of a team working together do define a domain specific language for their application is very interesting too - this DSL can guide developers when it comes to describing their app and designing tests at the appropriate level of functionality. That is, it can help developers understand the bigger picture of functionality before they get involved with implementation details. It can also help developers communicate at the appropriate level with non-developers, as instead of talking about implementation details when discussing the system, they can talk in the common language of the business.
1. Test driven development. This is my preferred way of writing code. Although I'm very aware that not all developers like to work this way, and there are many thousands of great developers who don't adopts this approach. But even if we don't agree with "pure TDD", at least we agree with writing tests. I do tend to side with the Ruby on Rails community when they say integration tests are just fine, and tdd can be overkill: if your integration tests run really fast anyway, then testing well at this level is arguably good enough - and better than trying to decouple all the code and make it testable at a unit level...
1. Pair programming. Pair programming isn't so common, but it really can ensure a high quality standard. When developers work on a task together and share the programming challenge, they tend to think more clearly about the issue at hand, improving the quality of their understanding and therefore the quality of the solution. Also, the code review is continuous, so there's a far greater chance of issues being caught early.
1. Deployment to different environments. Developers should be testing their code locally, but also integrating it and testing things in a deployed environment (often called "dev"). If they're happy with how things work, then the code should be deployed to a test environment where dedicated testers can explore things. If everything looks good here, then the code can be promoted to a staging environment, which as as close to production as possible. A final check of the app can be made here before signing off deployment to production.

### Regarding testing, where does a unit and integration test begin and end? That is, what are their differences?

I think that if we follow strict definitions, then a unit test will test a single unit of code, or a given unit of functionality within a module, while an integration test is anything that tests the integration of more than one unit of code.

For me, the key feature of a unit test is that it tests the logic of an application and it runs in-memory. That is, unit tests tend to focus more on the "business logic" within an application, or the original code developers have actually written themselves to solve a problem. Unlike integration tests, unit tests shouldn't involve frameworks, plug-ins or third party modules.

This small app shows us this distinction between unit and integration tests. There isn't a lot of non-framework code in the app - only a small amount of logic relating to field validation. This code is tested directly by the unit tests - they stub out the SQLAlchemy code and ignore the FastAPI framework to just trigger and test this logic directly. There are more integration tests. At the integration test level, we start to test the code around this logic, i.e. the FastAPI code and the SQLAlchemy code. The tests cover different areas of functionality, ensuring that everything works together as expected.

End-to-end tests are arguably integration tests too. They test multiple units of functionality, but often run "out of process" - i.e. the app is run in one process (typically, a server or a docker image) and the tests run in another process. They differ from integration tests in the sense that they typically have far less control over the application. As integration tests run in the same process as the system under test, they can "hook in" to the application to control it in certain ways that aid the testing. For example, the integration tests in this project rely on the TestClient from FastAPI, which simplifies testing of the RESTful interface. The end to end tests rely on the Requests library to make HTTP calls, simulating more closely how the application will be used "in the real world".


### How can you measure the code quality of this project? What metrics/characteristics make up quality?

A lot of teams rely on the test coverage metric to give them a measure of "code quality". It can be a useful metric for teams that are keen to write unit and integration tests for their work. Many teams will agree to a "minimum level" of code coverage for their app, and they can implement a CI step that will reject any PRs that take test coverage below this level.

There are linting tools available that also check for syntax issues and questions of style. For example, I used pylint to help me notice small things in the code that could be "improved". A big benefit of linters is that they can help developers on a team maintain the same presentation style when writing code. Most style rules are arbitrary, and different developers will typically have different opinions: using a linter to enforce the style rules just makes it clear to developers how their team has agreed to write code.

With the arrival of AI-powered code analysis, it's also become easier to identify and improve blocks of code that could be hard to understand. Functions with lots of lines, or conditionals with lots of branches are often picked up on as "difficult to understand". These can be identified by static analysis tools, and AI tooling can even offer suggestions for how to rewrite the code more intelligibly.

That said, the concept of "technical debt" is often at the forefront of a developer's mind when writing or reviewing code. "Technical debt" is generally understood to be "poor quality" code that would ideally be written more nicely. However, it's not so clear that all "poor quality" code needs to be improved. There is a line of thinking that would argue that a "poor quality" function that works fine and never needs to be modified or understood deeply by a developer, is a low priority candidate for fixing. The technical debt we want to fix is code that developers need to read and understand frequently, or code that gets modified a lot. In this case, it's important to improve the quality of the code, so that developers can understand it faster and modify it easiliy without risking the introduction of bugs or breakages to the logic.