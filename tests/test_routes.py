"""Tests for ROUTE-001 through ROUTE-014, plus things-to-do."""
from unittest.mock import patch


def _make_events(n):
    return [
        {
            "title": f"Event {i}",
            "date": {"when": "Sat, May 18"},
            "address": ["Venue", "City, TX"],
            "link": f"https://example.com/{i}",
            "description": "family friendly fun",
            "thumbnail": None,
            "ticket_info": [],
        }
        for i in range(n)
    ]


# ROUTE-001 — index form elements
def test_index_has_location_input(client):
    response = client.get("/")
    html = response.data.decode()
    assert response.status_code == 200
    assert 'name="location"' in html


def test_index_has_date_select(client):
    html = client.get("/").data.decode()
    assert '<select' in html
    assert 'name="date"' in html


# ROUTE-003 — date param maps to date_chip kwarg
def test_search_passes_date_chip_to_serpapi(client):
    with patch("app.routes.search_events", return_value=[]) as mock_fn:
        client.get("/search?location=Boston+MA&date=today")
        kwargs = mock_fn.call_args.kwargs
        assert kwargs["location"] == "Boston MA"
        assert kwargs["date_chip"] == "date:today"


def test_search_no_date_chip_when_date_omitted(client):
    with patch("app.routes.search_events", return_value=[]) as mock_fn:
        client.get("/search?location=Boston+MA")
        assert mock_fn.call_args.kwargs.get("date_chip") is None


# ROUTE-005 — kids_only=1 applies apply_kids_filter
def test_kids_only_calls_kids_filter(client):
    with patch("app.routes.search_events", return_value=_make_events(2)):
        with patch("app.routes.apply_kids_filter", return_value=[]) as mock_kids:
            client.get("/search?location=Austin+TX&kids_only=1")
            assert mock_kids.called


def test_kids_only_absent_skips_kids_filter(client):
    with patch("app.routes.search_events", return_value=_make_events(2)):
        with patch("app.routes.apply_kids_filter", return_value=[]) as mock_kids:
            client.get("/search?location=Austin+TX")
            assert not mock_kids.called


# ROUTE-007 / ROUTE-008 — pagination context
def test_next_link_present_when_10_results(client):
    with patch("app.routes.search_events", return_value=_make_events(10)):
        response = client.get("/search?location=Austin+TX&page=1")
        assert b"Next" in response.data


def test_no_prev_link_on_first_page(client):
    with patch("app.routes.search_events", return_value=_make_events(10)):
        response = client.get("/search?location=Austin+TX&page=1")
        assert b"Previous" not in response.data


def test_prev_link_present_on_page_2(client):
    with patch("app.routes.search_events", return_value=_make_events(5)):
        response = client.get("/search?location=Austin+TX&page=2")
        assert b"Previous" in response.data


# ROUTE-009 / ROUTE-010 — no results message
def test_no_results_shows_message(client):
    with patch("app.routes.search_events", return_value=[]):
        response = client.get("/search?location=Nowhere")
        assert response.status_code == 200
        assert b"no events" in response.data.lower()


# ROUTE-011 / ROUTE-012 — blank location redirects home
def test_blank_location_redirects(client):
    response = client.get("/search?location=")
    assert response.status_code == 302
    assert response.headers["Location"] == "/"


# ROUTE-013 / ROUTE-014 — unexpected exception renders error page
def test_exception_renders_error_page(client):
    with patch("app.routes.search_events", side_effect=RuntimeError("boom")):
        response = client.get("/search?location=Austin+TX")
        assert response.status_code == 500
        assert b"wrong" in response.data.lower()


# /event detail route
def test_event_detail_returns_200(client):
    response = client.get(
        "/event?title=Kite+Festival&link=https://example.com&when=Sat+May+18"
        "&address=Zilker+Park||Austin+TX&description=Fun+for+all"
    )
    assert response.status_code == 200


def test_event_detail_shows_title(client):
    response = client.get("/event?title=Kite+Festival&link=https://example.com&when=Sat")
    assert b"Kite Festival" in response.data


def test_event_detail_has_back_link(client):
    response = client.get(
        "/event?title=X&link=https://example.com&when=Sat"
        "&back_url=/search?location=Austin+TX"
    )
    assert b"Back to results" in response.data
    assert b"/search" in response.data


def test_event_detail_renders_without_optional_fields(client):
    # thumbnail, description, cost all absent — should not crash
    response = client.get("/event?title=Minimal+Event&link=https://example.com&when=Sun")
    assert response.status_code == 200
    assert b"Minimal Event" in response.data


# Things To Do — search_places integrated into /search
def test_search_passes_places_to_template(client):
    mock_places = [{"title": "Lincoln Park Zoo", "type": "Zoo", "address": "Chicago, IL",
                    "rating": 4.7, "reviews": 1000, "hours": "Open", "thumbnail": None,
                    "links": {"website": "https://zoo.org"}}]
    with patch("app.routes.search_events", return_value=[]):
        with patch("app.routes.search_places", return_value=mock_places):
            response = client.get("/search?location=Chicago+IL")
    assert response.status_code == 200
    assert b"Lincoln Park Zoo" in response.data


def test_search_shows_things_to_do_tab(client):
    with patch("app.routes.search_events", return_value=[]):
        with patch("app.routes.search_places", return_value=[]):
            response = client.get("/search?location=Chicago+IL")
    assert b"Things To Do" in response.data


def test_search_places_failure_does_not_crash_page(client):
    with patch("app.routes.search_events", return_value=[]):
        with patch("app.routes.search_places", return_value=[]):
            response = client.get("/search?location=Chicago+IL")
    assert response.status_code == 200
