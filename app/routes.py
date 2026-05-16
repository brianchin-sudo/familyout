from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.serpapi_client import search_events
from app.filters import apply_blocklist, apply_kids_filter

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
        events = apply_blocklist(events)
        if kids_only:
            events = apply_kids_filter(events)
    except Exception:
        return render_template("error.html"), 500

    return render_template(
        "results.html",
        events=events,
        location=location,
        page=page,
        has_prev=page > 1,
        has_next=len(events) >= 10,
        date=date_val,
        category=category,
        kids_only=kids_only,
    )
