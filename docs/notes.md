# Notes

| Book | Website |  Start Date | End Date |
| --- | --- | --- | --- |
| Test-Driven Development With Python | https://www.obeythetestinggoat.com/ | 2020-09-01 | In Progress |

## Unstructured Notes

- In TDD the first step is always the same: write a test.
- First we write the test; then we run it and check that it fails as expected. Only then do we go ahead and build some 
of our app.
- The `unittest` module provides a nicer interface on writing test cases, a much better upgrade than just using `assert`
statements. A particular advantage is that the `unittest.TestCase` class has the `setUp` and `tearDown` methods that we
can use to execute commands before and after the tests had run.

## Terminologies and Concepts


- Functional Test == Acceptance Test == End-to-End Test
- User Story
    - A description of how the application will work from the point of view of the user. Used to structure a functional test.
- Expected failure
    - When a test fails in the way that we expected it to.

