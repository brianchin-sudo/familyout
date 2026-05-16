BLOCKLIST = {
    "21+", "nightclub", "bar crawl", "adult", "explicit",
    "18+", "brewery tour", "wine tasting", "cocktail",
}

KIDS_KEYWORDS = {"kids", "children", "family", "all ages", "toddler"}


def apply_blocklist(events):
    def is_clean(event):
        text = f"{event.get('title', '')} {event.get('description', '')}".lower()
        return not any(term in text for term in BLOCKLIST)
    return [e for e in events if is_clean(e)]


def apply_kids_filter(events):
    def has_family_content(event):
        text = f"{event.get('title', '')} {event.get('description', '')}".lower()
        return any(kw in text for kw in KIDS_KEYWORDS)
    return [e for e in events if has_family_content(e)]


def is_family_friendly(event):
    text = f"{event.get('title', '')} {event.get('description', '')}".lower()
    return any(kw in text for kw in KIDS_KEYWORDS)
