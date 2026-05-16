# Project Requirements Document

## Family-Friendly Events Finder

**Version:** 1.0  
**Date:** 2026-05-16

---

## Overview

A Python web application that helps families discover local, age-appropriate events using the SerpAPI Google Events API. Users can search by location and date range and get curated results filtered for family-friendly content.

---

## Goals

- Provide a simple, clean interface for families to find events near them
- Surface relevant event details (venue, time, cost, age suitability) at a glance
- Reduce noise by filtering out adult-oriented or unsuitable content

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11+ |
| Web Framework | Flask or FastAPI |
| Frontend | Jinja2 templates + vanilla CSS (or Tailwind CDN) |
| Events Data | SerpAPI — Google Events engine |
| Environment Config | `python-dotenv` |
| HTTP Client | `requests` or `httpx` |

---

## Functional Requirements

### 1. Search

- **FR-1.1** User can enter a location (city, ZIP code, or address)
- **FR-1.2** User can select a date range (today, this weekend, this week, next 7 days, custom)
- **FR-1.3** User can optionally filter by event category (outdoor, arts, sports, education, festivals)
- **FR-1.4** Search submits a query to SerpAPI Google Events engine with the provided parameters

### 2. Results

- **FR-2.1** Display a list of events returned by SerpAPI
- **FR-2.2** Each event card shows: title, date/time, venue name, address, thumbnail (if available), and a link to the original event page
- **FR-2.3** Indicate estimated cost or "Free" when available
- **FR-2.4** Paginate results if more than 10 events are returned

### 3. Family-Friendly Filtering

- **FR-3.1** Apply a keyword blocklist to exclude events flagged as adult-oriented (e.g., "21+", "bar crawl", "nightclub", "comedy club — explicit")
- **FR-3.2** Append family-friendly intent to the SerpAPI query string (e.g., `"family friendly"`, `"kids"`, `"all ages"`)
- **FR-3.3** Allow user to toggle a "Kids OK" badge filter to show only events that explicitly mention children

### 4. Event Detail

- **FR-4.1** Clicking an event opens a detail view (or modal) with full description, map link, and source link
- **FR-4.2** Detail view shows any age recommendations parsed from the description when available

### 5. No Authentication Required

- The app is publicly accessible with no login

---

## Non-Functional Requirements

- **NFR-1** Page load for search results < 3 seconds under normal network conditions
- **NFR-2** SerpAPI key stored in environment variable, never hard-coded or committed
- **NFR-3** Graceful error page when SerpAPI quota is exceeded or network fails
- **NFR-4** Mobile-responsive layout
- **NFR-5** No user data is stored; all searches are stateless

---

## SerpAPI Integration

### Endpoint

`GET https://serpapi.com/search`

### Required Parameters

| Parameter | Value |
|---|---|
| `engine` | `google_events` |
| `q` | `{user query} family friendly` |
| `location` | User-provided location string |
| `api_key` | `SERPAPI_KEY` env var |

### Optional Parameters

| Parameter | Purpose |
|---|---|
| `htichips` | Date range chip (e.g., `date:today`, `date:this_week`, `date:this_weekend`) |
| `start` | Offset for pagination (increments of 10) |

### Response Fields Used

- `events_results[].title`
- `events_results[].date.start_date` / `.when`
- `events_results[].address`
- `events_results[].link`
- `events_results[].thumbnail`
- `events_results[].description`
- `events_results[].ticket_info`

---

## Project Structure

```
serpapi-challenge/
├── app/
│   ├── __init__.py
│   ├── routes.py          # Flask/FastAPI route handlers
│   ├── serpapi_client.py  # SerpAPI wrapper + filtering logic
│   └── filters.py         # Family-friendly keyword blocklist
├── templates/
│   ├── base.html
│   ├── index.html         # Search form
│   ├── results.html       # Event list
│   └── detail.html        # Single event view
├── static/
│   └── style.css
├── .env.example           # Template for required env vars
├── requirements.txt
├── PRD.md
└── README.md
```

---

## Environment Variables

```
SERPAPI_KEY=your_key_here
FLASK_ENV=development
```

---

## Out of Scope (v1)

- User accounts or saved searches
- Email/push notifications for upcoming events
- Map view (pins/clusters)
- Crowd-sourced event submissions
- Recommendation engine or personalization

---

## Success Criteria

- A user can search for family-friendly events in any US city and receive relevant results within 3 seconds
- Zero adult-content events appear in results for a default search
- The app runs locally with `flask run` after setting one environment variable
