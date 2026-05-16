import os
import requests


SERPAPI_URL = "https://serpapi.com/search"


def search_events(location, query="family friendly", date_chip=None, page=1, category=None):
    api_key = os.environ.get("SERPAPI_KEY", "")
    if not api_key:
        return []

    base_q = query if "family friendly" in query else f"{query} family friendly"
    full_q = f"{category} {base_q}" if category and category != "all" else base_q

    start = (page - 1) * 10
    params = {
        "engine": "google_events",
        "q": full_q,
        "location": location,
        "api_key": api_key,
    }
    # SerpAPI Events rejects start=0 without a date chip — only send when paginating
    if start:
        params["start"] = start
    if date_chip:
        params["htichips"] = date_chip

    try:
        resp = requests.get(SERPAPI_URL, params=params, timeout=10)
        if resp.status_code != 200:
            return []
        return resp.json().get("events_results", [])
    except requests.RequestException:
        return []


def search_places(location, query="family friendly things to do"):
    api_key = os.environ.get("SERPAPI_KEY", "")
    if not api_key:
        return []

    params = {
        "engine": "google_local",
        "q": query,
        "location": location,
        "api_key": api_key,
    }

    try:
        resp = requests.get(SERPAPI_URL, params=params, timeout=10)
        if resp.status_code != 200:
            return []
        return resp.json().get("local_results", [])
    except requests.RequestException:
        return []
