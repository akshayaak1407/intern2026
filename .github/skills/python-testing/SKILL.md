---
name: python-testing
description: 'Python testing skill for writing pytest-based tests for this repository.'
---

Use this skill when asked to add, update, or improve Python tests.

Guidelines:
- Use `pytest` for all tests.
- Write test functions instead of test classes.
- Use fixtures for shared setup, where appropriate.
- Use `pytest.mark.parametrize` for table-driven test cases.
- Keep one `assert` per test function.
- Give tests descriptive names that explain the scenario and expected behavior.
- Avoid introducing tests that rely on external resources unless the project already uses them.
