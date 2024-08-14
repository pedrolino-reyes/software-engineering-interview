# How I went about the technical challenge

I thought I'd include a file to explain how I worked through this technical challenge, with some notes to explain the decisions that were made.

## Starting out - e2e tests

I looked at the requirements of the challenge and started thinking about how to go about the unit tests. I realised I'd want to do some code refactoring to make the code testable. But before jumping in and changing things, I first wanted to make sure I had a way of doing so safely, so I decided to start with e2e tests to cover the functionality.

The fact that I wanted to cover as much functionality as possible with the e2e tests may have led me to write more e2e tests than would ideally be necessary - for example validating field lengths and data types is perhaps not best done by an e2e test, but should be tested lower down in unit or integration tests. But since I didn't have tests at this level, and since adding e2e tests for these aspects of the system was easy enough, I decided to include these tests.

I made the decision to control the database with these tests and added a fixture that initialised the database in a known state and then truncated all the data at the end of the test run. I did this to simplify some of the tests. It's not always possible to do this in e2e tests, where you might not have control of the database being used on a test server for example, but it was possible here so I went ahead...

In writing the e2e tests, I uncovered some of the issues that the readme file told me to expect. I found the following issues thanks to the e2e tests, and fixed them before proceeding:

1. The update endpoint didn't update the task description at all. The other fields were updated correctly.
1.


# New python libraries

I installed the following libraries using poetry (this is reflected in the change to pyproject.toml):

- pytest
- pytest-cov
- requests


# Other things I did

I moved the .gitignore file to the root of the repo. I'd opened files on a Mac, which had added .DS_Store files at levels above the `fastapi` folder, and I wanted to ignore them all.

I use