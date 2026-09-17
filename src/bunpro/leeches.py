"""Script Filter: BunPro leeches (ghost-SRS items you keep missing)."""

import datetime as dt
import os
import sys

from alfred_items import emit, error_item, item
from bunpro_api import BunproError, get_ghost_leeches

DASHBOARD_URL = "https://bunpro.jp/dashboard"
ICON = "icons/icon_leeches.png"
MAX_RESULTS = 10
ONE_HOUR_SECONDS = 3600
ONE_DAY_SECONDS = 86400


def _parse(timestamp: str) -> dt.datetime:
    return dt.datetime.fromisoformat(timestamp.replace("Z", "+00:00"))


def _next_review_subtitle(next_review: str, now: dt.datetime) -> str:
    delta = (_parse(next_review) - now).total_seconds()
    if delta <= 0:
        return "next review: now"
    if delta < ONE_HOUR_SECONDS:
        return f"next review in {int(delta // 60)}m"
    if delta < ONE_DAY_SECONDS:
        return f"next review in {int(delta // ONE_HOUR_SECONDS)}h"
    return f"next review in {int(delta // ONE_DAY_SECONDS)}d"


def select_leeches(reviews: list[dict]) -> list[dict]:
    active = [r for r in reviews if not r["attributes"]["is_slain"]]
    return sorted(active, key=lambda r: r["attributes"]["streak"])[:MAX_RESULTS]


def build_items(reviews: dict, now: dt.datetime) -> list[dict]:
    included_by_key = {(i["type"], i["id"]): i for i in reviews.get("included", [])}
    leeches = select_leeches(reviews.get("data", []))

    if not leeches:
        return [item(title="🎉 No leeches - clean SRS!", valid=False)]

    items = []
    for review in leeches:
        attrs = review["attributes"]
        reviewable_ref = review["relationships"]["reviewable"]["data"]
        reviewable = included_by_key.get(
            (reviewable_ref["type"], reviewable_ref["id"]), {}
        ).get("attributes", {})
        title = reviewable.get("title", f"#{attrs['reviewable_id']}")
        meaning = reviewable.get("meaning", "")

        items.append(
            item(
                title=f"{title} - {meaning}",
                subtitle=(
                    f"streak {attrs['streak']} · "
                    f"{_next_review_subtitle(attrs['next_review'], now)}"
                ),
                arg=DASHBOARD_URL,
                icon=ICON,
            )
        )
    return items


def main() -> None:
    token = os.environ.get("BUNPRO_API_TOKEN", "").strip()
    if not token:
        emit(
            [
                error_item(
                    "No BunPro API token set - add it in the workflow configuration"
                )
            ]
        )
        return

    try:
        reviews = get_ghost_leeches(token)
    except BunproError as error:
        emit([error_item(str(error))])
        return

    emit(build_items(reviews, dt.datetime.now(dt.UTC)))


if __name__ == "__main__":
    sys.exit(main())
