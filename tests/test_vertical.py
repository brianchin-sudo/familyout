"""Phase 1 vertical slice tests."""
import responses as rsps_lib
import responses


def test_index_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200


@responses.activate
def test_search_returns_200_with_events_text(client, mock_serpapi_response):
    rsps_lib.add(
        rsps_lib.GET,
        "https://serpapi.com/search",
        json=mock_serpapi_response,
        status=200,
    )
    response = client.get("/search?location=Austin+TX")
    assert response.status_code == 200
    assert b"events" in response.data.lower()
    # Smoke test note: real API confirmed working 2026-05-16 with Austin TX query
