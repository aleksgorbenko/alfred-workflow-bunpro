"""Script Filter: BunPro SRS stage breakdown (grammar + vocab)."""

import os
import sys

from alfred_items import emit, error_item, item
from bunpro_api import BunproError, get_srs_level_overview

DASHBOARD_URL = "https://bunpro.jp/dashboard"

STAGES = [
    ("beginner", "Beginner"),
    ("adept", "Adept"),
    ("seasoned", "Seasoned"),
    ("expert", "Expert"),
    ("master", "Master"),
]


def build_items(overview: dict) -> list[dict]:
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
        overview = get_srs_level_overview(token)
    except BunproError as error:
        emit([error_item(str(error))])
        return

    emit(build_items(overview))


if __name__ == "__main__":
    sys.exit(main())
