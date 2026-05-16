# Terms that clearly signal adult-only events
BLOCKLIST = {
    "21+", "nightclub", "bar crawl", "explicit",
    "18+", "brewery tour", "wine tasting", "cocktail",
}

# "adult" is too broad for places (catches "adult ticket pricing" at family venues)
# so it's only added when filtering events
EVENTS_BLOCKLIST = BLOCKLIST | {"adult"}

KIDS_KEYWORDS = {"kids", "children", "family", "all ages", "toddler"}


def apply_blocklist(items, blocklist=None):
    if blocklist is None:
        blocklist = BLOCKLIST

    def is_clean(item):
        text = f"{item.get('title', '')} {item.get('description', '')}".lower()
        return not any(term in text for term in blocklist)

    return [item for item in items if is_clean(item)]


def apply_kids_filter(events):
    def has_family_content(event):
        text = f"{event.get('title', '')} {event.get('description', '')}".lower()
        return any(kw in text for kw in KIDS_KEYWORDS)
    return [e for e in events if has_family_content(e)]


def hires_thumb(url):
    """Strip Google's &s (small) suffix to get a higher-resolution thumbnail."""
    if url and "encrypted-tbn" in url and url.endswith("&s"):
        return url[:-2]
    return url


def is_family_friendly(event):
    text = f"{event.get('title', '')} {event.get('description', '')}".lower()
    return any(kw in text for kw in KIDS_KEYWORDS)
