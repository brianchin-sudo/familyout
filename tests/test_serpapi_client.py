"""Tests for SERP-001/002, SERP-003/004, SERP-005/006, SERP-012/013."""
import requests as req_lib
import responses
from urllib.parse import urlparse, parse_qs

from app.serpapi_client import search_events

SEARCH_URL = "https://serpapi.com/search"


# SERP-001 / SERP-002 — query always contains "family friendly"
@responses.activate
def test_query_contains_family_friendly():
    responses.add(responses.GET, SEARCH_URL, json={"events_results": []}, status=200)
    search_events(location="Denver CO")
    params = parse_qs(urlparse(responses.calls[0].request.url).query)
    assert "family friendly" in params["q"][0]


@responses.activate
def test_custom_query_still_appends_family_friendly():
    responses.add(responses.GET, SEARCH_URL, json={"events_results": []}, status=200)
    search_events(location="Denver CO", query="outdoor")
    params = parse_qs(urlparse(responses.calls[0].request.url).query)
    assert "family friendly" in params["q"][0]
    assert "outdoor" in params["q"][0]


# SERP-003 / SERP-004 — date_chip maps to htichips
@responses.activate
def test_date_chip_sent_as_htichips():
    responses.add(responses.GET, SEARCH_URL, json={"events_results": []}, status=200)
    search_events(location="Denver CO", date_chip="date:today")
    params = parse_qs(urlparse(responses.calls[0].request.url).query)
    assert params["htichips"][0] == "date:today"


@responses.activate
def test_no_htichips_when_date_chip_omitted():
    responses.add(responses.GET, SEARCH_URL, json={"events_results": []}, status=200)
    search_events(location="Denver CO")
    params = parse_qs(urlparse(responses.calls[0].request.url).query)
    assert "htichips" not in params


# SERP-005 / SERP-006 — pagination maps page to start offset
@responses.activate
def test_page_1_omits_start_param():
    responses.add(responses.GET, SEARCH_URL, json={"events_results": []}, status=200)
    search_events(location="Denver CO", page=1)
    params = parse_qs(urlparse(responses.calls[0].request.url).query)
    # start=0 breaks SerpAPI Events without a date chip — omit it on page 1
    assert "start" not in params


@responses.activate
def test_page_2_sets_start_10():
    responses.add(responses.GET, SEARCH_URL, json={"events_results": []}, status=200)
    search_events(location="Denver CO", page=2)
    params = parse_qs(urlparse(responses.calls[0].request.url).query)
    assert params["start"][0] == "10"


# SERP-012 / SERP-013 — graceful error handling
@responses.activate
def test_returns_empty_list_on_non_200():
    responses.add(responses.GET, SEARCH_URL, status=500)
    assert search_events(location="Denver CO") == []


@responses.activate
def test_returns_empty_list_on_network_error():
    responses.add(
        responses.GET,
        SEARCH_URL,
        body=req_lib.exceptions.ConnectionError("network error"),
    )
    assert search_events(location="Denver CO") == []
