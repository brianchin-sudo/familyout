"""Tests for UI-002, UI-004."""
from unittest.mock import patch


# UI-002 — index.html has required form fields
def test_index_has_location_input(client):
    html = client.get("/").data.decode()
    assert '<form' in html
    assert 'name="location"' in html


def test_index_has_date_select(client):
    html = client.get("/").data.decode()
    assert 'name="date"' in html


# UI-004 — results.html renders event cards
def test_results_renders_two_event_cards(client, mock_serpapi_response):
    with patch("app.routes.search_events", return_value=mock_serpapi_response["events_results"]):
        response = client.get("/search?location=Austin+TX")
    html = response.data.decode()
    assert html.count('class="event-card"') == 2


def test_results_card_contains_title(client, mock_serpapi_response):
    with patch("app.routes.search_events", return_value=mock_serpapi_response["events_results"]):
        response = client.get("/search?location=Austin+TX")
    assert b"Family Fun Day" in response.data


def test_results_card_contains_venue(client, mock_serpapi_response):
    with patch("app.routes.search_events", return_value=mock_serpapi_response["events_results"]):
        response = client.get("/search?location=Austin+TX")
    assert b"Zilker Park" in response.data
