from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.serpapi_client import search_events, search_places
from app.filters import apply_blocklist, apply_kids_filter, EVENTS_BLOCKLIST

bp = Blueprint("main", __name__)

DATE_CHIP_MAP = {
    "today": "date:today",
    "this_weekend": "date:this_weekend",
    "this_week": "date:this_week",
    "next_7_days": "date:next_7_days",
}


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/search")
def search():
    location = request.args.get("location", "").strip()
    if not location:
        flash("Please enter a location.")
        return redirect(url_for("main.index"))

    date_val = request.args.get("date", "")
    date_chip = DATE_CHIP_MAP.get(date_val)
    category = request.args.get("category", "all")
    kids_only = request.args.get("kids_only", "") == "1"
    page = max(1, int(request.args.get("page", 1)))

    try:
        events = search_events(
            location=location,
            date_chip=date_chip,
            page=page,
            category=category,
        )
        events = apply_blocklist(events, blocklist=EVENTS_BLOCKLIST)
        if kids_only:
            events = apply_kids_filter(events)
    except Exception:
        return render_template("error.html"), 500

    # Places search is best-effort — never let its failure break the events page
    try:
        places = apply_blocklist(search_places(location))
    except Exception:
        places = []

    return render_template(
        "results.html",
        events=events,
        places=places,
        location=location,
        page=page,
        has_prev=page > 1,
        has_next=len(events) >= 10,
        date=date_val,
        category=category,
        kids_only=kids_only,
    )


@bp.route("/event")
def event_detail():
    event = {
        "title":       request.args.get("title", ""),
        "link":        request.args.get("link", ""),
        "thumbnail":   request.args.get("thumbnail") or None,
        "date":        {"when": request.args.get("when", "")},
        "address":     request.args.get("address", "").split("||"),
        "description": request.args.get("description", ""),
        "ticket_info": [{"source": request.args.get("cost", "")}] if request.args.get("cost") else [],
    }
    back_url = request.args.get("back_url", url_for("main.index"))
    return render_template("detail.html", event=event, back_url=back_url)
