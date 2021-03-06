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
- Django provides a `LiveServerTestCase` class that gives some additionall functionalities for functional tests. At the
very least, it integrates the FTs onto the Django test runner so we can run the whole test suite with a single 
`python manage.py test` command


## Quick Tips

- When to commit?
    - Big changes to a functional test are usually a good thing to commit on their own.
    - It’s a good idea to do a commit after any refactoring:
- Unit tests are really about testing logic, flow control, and configuration. **Don't test constants**.

## Terminologies and Concepts

- Functional Test == Acceptance Test == End-to-End Test
- User Story
    - A description of how the application will work from the point of view of the user. Used to structure a functional test.
- Expected failure
    - When a test fails in the way that we expected it to.
- Functional vs Unit Tests
    - Functional tests test the application from the outside, from the point of view of the user.
    - Functional tests should help you build an application with the right functionality, and guarantee you never 
    accidentally break it. 
    - Unit tests test the application from the inside, from the point of view of the programmer.
    - Unit tests should help you to write code that’s clean and bug free. 
- The unit-test/code cycle
    1. Run the unit tests in the terminal.
    2. Make a minimal code change in the editor.
    3. Repeat!
- The TDD Process:
    1. We write a test. 
    2. We run the test and see it fail. 
    3. We write some minimal code to get it a little further. We rerun the test and repeat until it passes. 
    4. Then, optionally, we might refactor our code, using our tests to make sure we don’t break anything.
- Regression
    - When new code breaks some aspect of the application which used to work.

![](assets/overall-tdd-process.png)

- The TDD Process with Functional and Unit Tests:
    1. We write a functional test and see it fail.
    2. Then, the process of "writing code" to get it to pass is a mini-TDD cycle of its own: 
        - We write one or more unit tests, and go into the unit-test/code cycle until the unit tests pass. 
    3. Then, we go back to our FT to check that it gets a little further
    4. We can write a bit more of our application -- using more unit tests, and so on.
    
![](assets/tdd-process-with-functional-and-unit-tests.png)

- Red/Green/Refactor and Triangulation
    - Start by writing a unit test which fails (Red).
    - Write the simplest possible code to get it to pass (Green), even if that means cheating.
    - Refactor to get to better code that makes more sense.


## Code Smells

- A long unit test either needs to be broken into two, or it may be an indication that the thing you’re testing is 
too complicated.

## Testing Best Practices

- Ensure test isolation and manage global state
    - Different tests shouldn't affect one another.
    - Using `django.test.TestCase` and `django.test.LiveServerTestCase` helps with this
- Avoid "voodoo" sleeps
    - Hard coded `time.sleep()`s are not consistent enough considering different variables (device hanging, slow 
    connection, etc.) might affect the test results
    - Selenium has provided implicit waits, but the implementation varies across different browsers.  "Explicit is 
    better than implict", as the Zen of Python says!
- Styling shouldn't be tested, because that's essentialy the same as testing a constant.
    - Test the implementation instead (i.e. if the CSS files are loaded correctly)

## Quotables

On the purpose of TDD:

> Ultimately, programming is hard. Often, we are smart, so we succeed. TDD is there to help us out when we’re not so smart. 

On writing test for trivial functions:

> ...if they’re really trivial tests, then they won’t take you that long to write them. So stop moaning and just write them already.

On refactoring:

> When refactoring, work on either the code or the tests, but not both at once. 

On when to refactor:

> One methodology is eliminate duplication: if your test uses a magic constant, and your application code also uses it, 
that counts as duplication, so it justifies refactoring. 

If that still is too vauge:

> ... use Triangulation: if your tests let you get away with writing "cheating" code that you’re not happy with, like 
returning a magic constant, write another test that forces you to write some better code. 

On DRY (Don't Repeat Yourself):

> You can copy and paste code once, and it may be premature to try to remove the duplication it causes, but once you 
get three occurrences, it’s time to remove duplication.

On "Unit Tests Versus Integrated Tests, and the Database"

> It’s OK to ignore this distinction for now—we have two types of test, the high-level functional tests which test 
the application from the user’s point of view, and these lower-level tests which test it from the programmer’s point of
view.

On Working State to Working State:

> Our natural urge is often to dive in and fix everything at once… but if we’re not careful, we’ll end up [...] 
in a situation with loads of changes to our code and nothing working.

On splitting work out into small, achievable tasks 

> Sometimes this means starting with "boring" work rather than diving straight in with the fun stuff, but you’ll have 
to trust that YOLO-you in the parallel universe is probably having a bad time, having broken everything, and struggling
to get the app working again.

On YAGNI:

> Avoid the temptation to write code that you think might be useful, just because it suggests itself at the time. 

On real developers:

> Real developers ship