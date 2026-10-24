"""Script Filter: BunPro SRS stage breakdown (grammar + vocab)."""

from typing import Any

from alfred_items import item
from bunpro_api import get_srs_level_overview

DASHBOARD_URL = "https://bunpro.jp/dashboard"

STAGES = [
    ("beginner", "Beginner"),
    ("adept", "Adept"),
    ("seasoned", "Seasoned"),
    ("expert", "Expert"),
    ("master", "Master"),
]


def build_items(overview: dict[str, Any]) -> list[dict[str, Any]]:
    grammar = overview.get("grammar", {})
    vocab = overview.get("vocab", {})

    return [
        item(
            title=f"{label}: {grammar.get(key, 0) + vocab.get(key, 0)}",
            subtitle=f"Grammar {grammar.get(key, 0)} · Vocab {vocab.get(key, 0)}",
            arg=DASHBOARD_URL,
            icon=f"icons/icon_stage_{key}.png",
        )
        for key, label in STAGES
    ]


def load(token: str) -> list[dict[str, Any]]:
    return build_items(get_srs_level_overview(token))
