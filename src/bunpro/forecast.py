"""Script Filter: BunPro review forecast (grammar + vocab due per day)."""

import datetime as dt
from typing import Any

from alfred_items import item
from bunpro_api import get_forecast_daily

DASHBOARD_URL = "https://bunpro.jp/dashboard"
ICON = "icons/icon_forecast.png"

LABELS = {"later": "Later today", "tomorrow": "Tomorrow"}


def _label(key: str) -> str:
    if key in LABELS:
        return LABELS[key]
    date = dt.date.fromisoformat(key)
    return date.strftime("%a %d/%m")


def build_items(daily: dict[str, Any]) -> list[dict[str, Any]]:
    grammar = daily.get("grammar", {})
    vocab = daily.get("vocab", {})

    items: list[dict[str, Any]] = []
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


def load(token: str) -> list[dict[str, Any]]:
    return build_items(get_forecast_daily(token))
