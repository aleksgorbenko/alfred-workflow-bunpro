"""Script Filter: BunPro review forecast (grammar + vocab due per day)."""

import datetime as dt
import os
import sys

from alfred_items import emit, error_item, item
from bunpro_api import BunproError, get_forecast_daily

DASHBOARD_URL = "https://bunpro.jp/dashboard"
ICON = "icons/icon_forecast.png"

LABELS = {"later": "Later today", "tomorrow": "Tomorrow"}


def _label(key: str) -> str:
    if key in LABELS:
        return LABELS[key]
    date = dt.datetime.strptime(key, "%Y-%m-%d").date()
    return date.strftime("%a %d/%m")


def build_items(daily: dict) -> list[dict]:
    grammar = daily.get("grammar", {})
    vocab = daily.get("vocab", {})

    items = []
    for key in grammar:
        g_due = grammar.get(key, 0)
        v_due = vocab.get(key, 0)
        items.append(
            item(
                title=_label(key),
                subtitle=f"Grammar {g_due}, Vocab {v_due}",
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
        daily = get_forecast_daily(token)
    except BunproError as error:
        emit([error_item(str(error))])
        return

    emit(build_items(daily))


if __name__ == "__main__":
    sys.exit(main())
