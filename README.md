# FamilyOut

A Python/Flask web app that surfaces family-friendly events using the [SerpAPI Google Events engine](https://serpapi.com/google-events-api). Search by location and date, filter by category, and toggle a "Kids Only" mode to see only explicitly child-friendly events.

## Setup

```bash
# 1. Clone and enter the repo
git clone <repo-url>
cd serpapi-challenge

# 2. Copy the env template and add your SerpAPI key
cp .env.example .env
# Edit .env and set SERPAPI_KEY=your_key_here

# 3. Install dependencies
make install

# 4. Start the development server
make run
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

## Running tests

```bash
make test
```

With coverage report:

```bash
make test-cov
```

## Project structure

```
app/
  __init__.py       Flask app factory
  routes.py         Request handlers
  serpapi_client.py SerpAPI integration
  filters.py        Blocklist + kids filter
templates/
  base.html         Shared layout
  index.html        Search form
  results.html      Event grid + pagination
  detail.html       Single event view
  error.html        Error page
static/
  style.css         Mobile-first responsive styles
tests/
  conftest.py            Fixtures and shared mocks
  test_vertical.py       Phase 1 end-to-end smoke tests
  test_serpapi_client.py SerpAPI query/param/error tests
  test_filters.py        Blocklist and kids-filter unit tests
  test_routes.py         Flask route unit tests
  test_templates.py      Rendered HTML assertions
  test_integration.py    Full request-cycle integration tests
```

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `SERPAPI_KEY` | Yes | Your SerpAPI API key |
| `FLASK_ENV` | No | `development` enables debug mode |
| `FLASK_SECRET_KEY` | No | Secret key for flash messages (change in production) |

## Known behaviour

- **No date filter + page 1:** the SerpAPI Events engine rejects `start=0` without a date chip and returns no results. The app omits `start` on page 1 to avoid this. Pagination (`page=2+`) always includes `start`.
- **Missing API key:** a warning is logged at startup and all searches return "no events found" rather than crashing.
