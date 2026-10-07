# Walkthrough Script

## Introduction
"This project is an automated test suite covering both API and UI testing for two practice
applications: reqres.in for API CRUD/auth testing, and the Thinking Tester Contact List app for
end-to-end UI flows. It's built with pytest, Playwright, and Allure for reporting, with a CI
pipeline that runs on every push."

## Project structure
Open the repo in the editor and show, in order:
- `conftest.py` — point out the session-scoped `api_base_url`/`auth_token`/`session` fixtures;
  -"built once, shared by every test, so config lives in one place."
- `tests/api/` vs `tests/ui/` — the two suites, kept separate.
- `api/schema.py` — JSON schemas used to validate API response shapes, not just status codes.
- `.github/workflows/ci.yml` — mention it runs automatically on every push/PR.

Fixtures and schemas live once, centrally — tests themselves stay short and
readable because the setup/validation logic isn't duplicated in every file.

## Live demo: run the suite
```bash
pytest -v
```
While it runs:
- "API tests are hitting reqres.in directly — checking status codes, response time under
  2 seconds, and validating the JSON shape against a schema."
- "UI tests are driving a real browser through signup, login, adding a contact, and logout."

If time is short, run just one of each instead of the full suite:
```bash
pytest tests/api/test_users.py::TestCreateUser -v
pytest tests/ui/test_contact_list_ui.py::TestSignup -v --headed
```
The `--headed` UI run is worth showing live — watching the browser actually click through the
form is more convincing than a terminal log.

## Allure report
```bash
allure serve allure-results
```
In the browser that opens:
- passing test — show the `@allure.step` breakdown and an attached response body.
- **Graphs** tab — Severity chart (Blocker/Critical/Normal/Minor).
- **Behaviors** — tests grouped by feature/story.

**Talking point:** "This isn't just pass/fail — anyone reviewing this later can see *why* a test
failed, with the actual request/response attached, without re-running anything."

## CI pipeline 
Open the GitHub Actions tab for a recent run:
- The job steps running in order (checkout → install → Playwright → test → Allure).
- **Artifacts** - the downloadable Allure HTML report.

**Talking point:** "Every push gets tested automatically, and the full report is attached to the
run — no one has to run tests locally just to see whether something broke."

## Summary
"schema-validated API tests, real browser UI tests, centralized fixtures and config,
automatic CI on every push, and a reviewable Allure report for every run.
---

### Backup / if something breaks live
- Have a pre-generated `allure-report/` folder ready to open locally in case live network
  requests to the demo apps are slow or the Heroku dyno is cold-starting.
- Have one test's terminal output already captured as a screenshot, in case live execution
  misbehaves on the day.