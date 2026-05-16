"""
INT-002: full request cycle — mock SerpAPI, assert clean events render and
         blocklisted events are absent.
INT-004: event card hrefs point to source URLs (no broken/missing hrefs).
INT-006: missing SERPAPI_KEY returns empty results gracefully (no crash).
"""
import responses
from urllib.parse import urlparse, parse_qs

from app.serpapi_client import search_events

SEARCH_URL = "https://serpapi.com/search"

FAMILY_EVENT = {
    "title": "Family Kite Festival",
    "date": {"when": "Sat, May 23"},
    "address": ["Gas Works Park", "Seattle, WA"],
    "link": "https://example.com/kite-festival",
    "thumbnail": None,
    "description": "A family friendly kite festival for kids and parents.",
    "ticket_info": [{"source": "Free", "link": ""}],
}

ADULT_EVENT = {
    "title": "21+ Nightclub Bash",
    "date": {"when": "Sat, May 23"},
    "address": ["Some Bar", "Seattle, WA"],
    "link": "https://example.com/nightclub",
    "thumbnail": None,
    "description": "Adults only cocktail event.",
    "ticket_info": [],
}


# INT-002 — full cycle: good event renders, blocklisted event is stripped
@responses.activate
def test_search_renders_family_event_and_strips_blocklisted(client):
    responses.add(
        responses.GET,
        SEARCH_URL,
        json={"events_results": [FAMILY_EVENT, ADULT_EVENT]},
        status=200,
    )

    response = client.get("/search?location=Seattle+WA&date=this_weekend")

    assert response.status_code == 200
    assert b"Family Kite Festival" in response.data
    assert b"21+ Nightclub Bash" not in response.data


@responses.activate
def test_date_chip_forwarded_to_serpapi(client):
    responses.add(
        responses.GET,
        SEARCH_URL,
        json={"events_results": [FAMILY_EVENT]},
        status=200,
    )

    client.get("/search?location=Seattle+WA&date=this_weekend")

    params = parse_qs(urlparse(responses.calls[0].request.url).query)
    assert params["htichips"][0] == "date:this_weekend"


@responses.activate
def test_kids_only_strips_non_family_events(client):
    non_family = {**FAMILY_EVENT, "title": "Corporate Conference", "description": "Business event"}
    responses.add(
        responses.GET,
        SEARCH_URL,
        json={"events_results": [FAMILY_EVENT, non_family]},
        status=200,
    )

    response = client.get("/search?location=Seattle+WA&kids_only=1")

    assert b"Family Kite Festival" in response.data
    assert b"Corporate Conference" not in response.data


# INT-004 — event card links contain the source URL from the payload
@responses.activate
def test_event_card_links_use_source_url(client):
    responses.add(
        responses.GET,
        SEARCH_URL,
        json={"events_results": [FAMILY_EVENT]},
        status=200,
    )

    response = client.get("/search?location=Seattle+WA")

    assert b"https://example.com/kite-festival" in response.data


# INT-006 — missing API key returns empty results, no crash
def test_missing_api_key_returns_empty_list(monkeypatch):
    monkeypatch.delenv("SERPAPI_KEY", raising=False)
    result = search_events(location="Austin TX")
    assert result == []


def test_missing_api_key_shows_no_events_page(client, monkeypatch):
    monkeypatch.delenv("SERPAPI_KEY", raising=False)
    response = client.get("/search?location=Austin+TX")
    assert response.status_code == 200
    assert b"no events" in response.data.lower()
