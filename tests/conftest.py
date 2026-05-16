import pytest
from app import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def mock_serpapi_response():
    return {
        "events_results": [
            {
                "title": "Family Fun Day at the Park",
                "date": {"start_date": "May 18", "when": "Sat, May 18, 10 AM"},
                "address": ["Zilker Park", "Austin, TX"],
                "link": "https://example.com/event/1",
                "thumbnail": "https://example.com/thumb1.jpg",
                "description": "A fun family day with kids activities, games, and food. All ages welcome.",
                "ticket_info": [{"source": "Free", "link": ""}],
            },
            {
                "title": "Children's Science Expo",
                "date": {"start_date": "May 19", "when": "Sun, May 19, 11 AM"},
                "address": ["Austin Convention Center", "Austin, TX"],
                "link": "https://example.com/event/2",
                "thumbnail": None,
                "description": "Interactive science exhibits for children and families.",
                "ticket_info": [{"source": "Eventbrite", "link": "https://example.com/tickets/2"}],
            },
        ]
    }
