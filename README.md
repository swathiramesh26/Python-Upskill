PythonProject/
├── .env                     # Local config values (gitignored)
├── .env.example             # Template for .env — safe to commit
├── .gitignore
├── config.py                # Reads BASE_URL / BROWSER / HEADLESS from .env
├── conftest.py               # Shared fixtures (root-level)
├── pytest.ini                # Pytest config, custom markers
├── requirements.txt
├── run_tests.sh              # Convenience script — reads .env, runs pytest
│
├── pages/                    # Page Object Model
│   ├── __init__.py
│   └── todo_page.py          # TodoPage: locators + actions for TodoMVC
│
├── tests/                    # Test suites
│   ├── test_todomvc_suite.py       # Core 5-test TodoMVC suite
│   └── test_todo_data_driven.py    # Faker + JSON fixture data-driven tests
│
├── testdata/
│   └── todos.json            # Static test data
│
├── Exercises/                 # Standalone practice scripts (class-based BaseTest style)
│   └── week*_Exercises/

