# TASKS.md — Family-Friendly Events Finder

## How to Use

- **Complete phases in order.** Tasks within a phase's parallel groups can be handed to separate agents simultaneously.
- **TDD rule:** every implementation task is preceded by a test task. Write the test first, confirm it fails, then implement.
- Mark tasks complete with `[x]`.
- Task IDs are stable — reference them in commits and PRs.

---

## Phase 0 — Bootstrap
> **One agent. Must finish before anything else starts.**  
> Goal: a working skeleton with a test runner so all other agents have something to build on.

- [x] **BOOT-001** Create project directory structure: `app/`, `templates/`, `static/`, `tests/`
- [x] **BOOT-002** Create `requirements.txt` with: `flask`, `requests`, `python-dotenv`, `pytest`, `pytest-flask`, `responses` (HTTP mock library)
- [x] **BOOT-003** Create `.env.example` with `SERPAPI_KEY=` and `FLASK_ENV=development`
- [x] **BOOT-004** Create `app/__init__.py` that initializes a Flask app and loads `.env` via `python-dotenv`
- [x] **BOOT-005** Create `tests/conftest.py` with a `app` pytest fixture and a `client` fixture using Flask test client
- [x] **BOOT-006** Create `tests/conftest.py` entry: a `mock_serpapi_response` fixture that returns a hardcoded minimal SerpAPI events payload (2 events)
- [x] **BOOT-007** Confirm `pytest` runs and collects 0 tests with exit code 0

---

## Phase 1 — Minimal Vertical Slice
> **One agent. Run after Phase 0.**  
> Goal: the smallest possible working app — one search, one results page, real SerpAPI call. Proves the full stack before adding features.

- [x] **VERT-001** *(test)* Write `tests/test_vertical.py`: assert `GET /` returns HTTP 200
- [x] **VERT-002** Create `app/routes.py` with a single `GET /` route that renders `templates/index.html`; create a minimal `index.html` with a `<form>` containing a `location` text input and submit button
- [x] **VERT-003** *(test)* In `tests/test_vertical.py`: assert `GET /search?location=Austin+TX` returns HTTP 200 and response body contains the word "events" (case-insensitive)
- [x] **VERT-004** Create `app/serpapi_client.py` with a single function `search_events(location, query="family friendly")` that calls SerpAPI `google_events` engine and returns the raw `events_results` list (empty list on any error)
- [x] **VERT-005** Create `app/routes.py` `GET /search` route: call `search_events`, pass results to `templates/results.html`; create minimal `results.html` that loops over events and prints each title in a `<li>`
- [x] **VERT-006** *(smoke test)* With a real `SERPAPI_KEY` in `.env`, run `flask run`, open `http://localhost:5000`, submit "Austin TX" — confirm event titles appear in the browser. Document result in a comment in `tests/test_vertical.py`.

---

## Phase 2 — Feature Buildout
> **Start all four groups simultaneously after Phase 1.**  
> Each group is self-contained. Merge order does not matter.

---

### Group A — SerpAPI Client & Filtering
> Owns `app/serpapi_client.py` and `app/filters.py`

- [x] **SERP-001** *(test)* `tests/test_serpapi_client.py`: mock HTTP — assert that `search_events(location="Denver CO")` sends a request where `q` contains `"family friendly"`
- [x] **SERP-002** Update `search_events` to always append `"family friendly"` to the query string
- [x] **SERP-003** *(test)* Assert `search_events` passes the `htichips` parameter when `date_chip` argument is provided (e.g., `"date:today"`)
- [x] **SERP-004** Add `date_chip` optional argument to `search_events` that maps to the `htichips` SerpAPI parameter
- [x] **SERP-005** *(test)* Assert `search_events` passes `start` parameter correctly for page offsets (page 2 → `start=10`)
- [x] **SERP-006** Add `page` optional argument to `search_events`; compute `start = (page - 1) * 10`
- [x] **SERP-007** Create `app/filters.py` with `BLOCKLIST` — a set of lowercase strings: `{"21+", "nightclub", "bar crawl", "adult", "explicit", "18+", "brewery tour", "wine tasting", "cocktail"}`
- [x] **SERP-008** *(test)* `tests/test_filters.py`: assert `apply_blocklist(events)` removes any event whose title or description contains a blocklist term (case-insensitive); assert clean events pass through unchanged
- [x] **SERP-009** Implement `apply_blocklist(events: list) -> list` in `app/filters.py`
- [x] **SERP-010** *(test)* Assert `apply_kids_filter(events)` returns only events whose title or description contains at least one of: `"kids"`, `"children"`, `"family"`, `"all ages"`, `"toddler"`
- [x] **SERP-011** Implement `apply_kids_filter(events: list) -> list` in `app/filters.py`
- [x] **SERP-012** *(test)* Assert `search_events` returns an empty list (not an exception) when SerpAPI returns a non-200 status or a network error
- [x] **SERP-013** Wrap SerpAPI HTTP call in `search_events` with try/except; return `[]` on any `requests.RequestException` or non-200 response

---

### Group B — Flask Routes
> Owns `app/routes.py` and Flask error handlers

- [x] **ROUTE-001** *(test)* `tests/test_routes.py`: assert `GET /` renders a form with `name="location"` input and a date-range `<select>` element
- [x] **ROUTE-002** Update `index.html` to include: location text input, date-range select (`today`, `this_weekend`, `this_week`, `next_7_days`), category select (`all`, `outdoor`, `arts`, `sports`, `education`, `festivals`), and a "Kids Only" checkbox
- [x] **ROUTE-003** *(test)* Assert `GET /search?location=Boston+MA&date=today` calls `search_events` with `location="Boston MA"` and `date_chip="date:today"` (use `monkeypatch` or `unittest.mock.patch`)
- [x] **ROUTE-004** Update `GET /search` route to extract `date`, `category`, `kids_only`, and `page` query params and pass them to `search_events` and filters
- [x] **ROUTE-005** *(test)* Assert `GET /search?location=X&kids_only=1` applies `apply_kids_filter` to results
- [x] **ROUTE-006** Update `GET /search` to apply `apply_blocklist` always, and `apply_kids_filter` when `kids_only=1`
- [x] **ROUTE-007** *(test)* Assert `GET /search` response contains pagination links when results list has 10 items (next page link present) and first page has no "previous" link
- [x] **ROUTE-008** Implement pagination context: pass `page`, `has_next`, `has_prev` to `results.html`
- [x] **ROUTE-009** *(test)* Assert that when `search_events` returns `[]`, `GET /search` renders a "no events found" message and still returns HTTP 200
- [x] **ROUTE-010** Add no-results handling to `GET /search` route and `results.html`
- [x] **ROUTE-011** *(test)* Assert `GET /search` with a missing `location` param returns HTTP 400 with an error message
- [x] **ROUTE-012** Add input validation: redirect to `/` with a flash message if `location` is blank
- [x] **ROUTE-013** *(test)* Assert that when `search_events` raises an unexpected exception, the app renders `error.html` with HTTP 500 (not an unhandled crash)
- [x] **ROUTE-014** Register a Flask `500` error handler that renders `templates/error.html`

---

### Group C — UI Templates & Styles
> Owns `templates/` and `static/style.css`. No pytest tests — validate visually via `flask run`.

- [x] **UI-001** Create `templates/base.html`: `<!DOCTYPE html>`, viewport meta tag, link to `static/style.css`, `{% block content %}` slot, and a simple header with the app name "Family Events Finder"
- [x] **UI-002** *(test)* `tests/test_templates.py`: assert rendered `index.html` contains `<form`, `name="location"`, and `name="date"`
- [x] **UI-003** Update `templates/index.html` to extend `base.html`; style the search form with centered layout, large location input, and inline submit button
- [x] **UI-004** *(test)* Assert rendered `results.html` with 2 mock events contains 2 elements with class `event-card`
- [x] **UI-005** Build `templates/results.html`: extend `base.html`; render each event as an `.event-card` div showing thumbnail (if present), title as a link, date/time, venue + address, cost/free badge, and a "Kids OK" badge when keywords match
- [x] **UI-006** Add pagination controls to `results.html`: "Previous" and "Next" links that preserve all current query params
- [x] **UI-007** Build `templates/detail.html`: extend `base.html`; show full event description, embedded Google Maps link using venue address, source link button, and a back-to-results link
- [x] **UI-008** Build `templates/error.html`: extend `base.html`; friendly message ("Something went wrong — try a different search"), link back to home
- [x] **UI-009** Write `static/style.css`: mobile-first responsive grid for event cards (1 col on mobile, 2 on tablet, 3 on desktop); card hover state; badge styles for "Free" and "Kids OK"

---

### Group D — Config & Ops
> Owns repo-level files. Lightweight — can be done alongside any other group.

- [x] **OPS-001** Create `.gitignore`: `*.pyc`, `__pycache__/`, `.env`, `venv/`, `.pytest_cache/`, `*.egg-info/`
- [x] **OPS-002** Create `Makefile` with targets: `install` (pip install -r requirements.txt), `run` (flask run), `test` (pytest -v), `test-cov` (pytest --cov=app)
- [x] **OPS-003** Add `pytest-cov` to `requirements.txt`
- [x] **OPS-004** Create `README.md` with: project description, setup steps (clone → copy `.env.example` → add key → `make install` → `make run`), and a `make test` usage note

---

## Phase 3 — Integration & Polish
> **One agent. Run after all Phase 2 groups are merged.**  
> Goal: wire everything together, run the full test suite, fix any integration gaps.

- [x] **INT-001** Run `make test` — fix any test failures caused by merging Phase 2 groups
- [x] **INT-002** *(test)* `tests/test_integration.py`: full request cycle test — mock SerpAPI response, `GET /search?location=Seattle+WA&date=this_weekend` — assert results page renders event titles from the mock payload and blocklist events are absent
- [x] **INT-003** End-to-end smoke test with real API key: search "Chicago IL", "this weekend", Kids Only checked — verify no adult events appear, pagination works, detail view opens
- [x] **INT-004** Check all event card links open correct source URLs (no broken hrefs)
- [ ] **INT-005** Validate mobile layout in browser DevTools at 375px width — cards stack vertically, form is usable *(manual — open browser at 375px)*
- [x] **INT-006** Confirm `SERPAPI_KEY` missing from environment shows a clear startup error message rather than crashing silently on first search
- [x] **INT-007** Run `pytest --cov=app` — ensure line coverage ≥ 80% for `serpapi_client.py` and `filters.py`
