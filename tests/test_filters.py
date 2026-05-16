"""Tests for SERP-007/008/009, SERP-010/011."""
from app.filters import apply_blocklist, apply_kids_filter

CLEAN = {"title": "Science Fair", "description": "Educational activities for all ages"}
ADULT = {"title": "Nightclub Night", "description": "Dance until dawn"}
FAMILY = {"title": "Family Festival", "description": "Fun for everyone"}
NO_KW = {"title": "Corporate Gala", "description": "Black tie event"}


# SERP-008 / SERP-009 — apply_blocklist
def test_blocklist_removes_adult_events():
    result = apply_blocklist([ADULT, CLEAN])
    assert len(result) == 1
    assert result[0]["title"] == "Science Fair"


def test_blocklist_passes_clean_events_unchanged():
    result = apply_blocklist([CLEAN])
    assert result == [CLEAN]


def test_blocklist_case_insensitive():
    event = {"title": "21+ Bar Crawl Special", "description": "Adults only"}
    assert apply_blocklist([event]) == []


def test_blocklist_matches_description():
    event = {"title": "Saturday Night", "description": "Cocktail hour included"}
    assert apply_blocklist([event]) == []


def test_blocklist_empty_input():
    assert apply_blocklist([]) == []


# SERP-010 / SERP-011 — apply_kids_filter
def test_kids_filter_keeps_family_events():
    result = apply_kids_filter([FAMILY, NO_KW])
    assert len(result) == 1
    assert result[0]["title"] == "Family Festival"


def test_kids_filter_matches_description_keywords():
    event = {"title": "Saturday Show", "description": "Great for kids and toddlers"}
    assert apply_kids_filter([event]) == [event]


def test_kids_filter_matches_all_ages():
    event = {"title": "Community Day", "description": "All ages welcome"}
    assert apply_kids_filter([event]) == [event]


def test_kids_filter_removes_non_family_events():
    assert apply_kids_filter([NO_KW]) == []


def test_kids_filter_empty_input():
    assert apply_kids_filter([]) == []
