"""Script Filter: BunPro JLPT progress (grammar + vocab per N-level)."""

import os
import sys

from alfred_items import bold, emit, error_item, item
from bunpro_api import BunproError, get_jlpt_progress

DASHBOARD_URL = "https://bunpro.jp/dashboard"
ICON = "icons/icon_levels.png"
MASTERED_STAGES = ("expert", "master")


def _progress(level_stats: dict) -> tuple[int, int, int]:
    stages = ("beginner", "adept", "seasoned", "expert", "master")
    started = sum(level_stats.get(stage, 0) for stage in stages)
    mastered = sum(level_stats.get(stage, 0) for stage in MASTERED_STAGES)
    total = level_stats.get("total_count", 0)
    return started, mastered, total


def build_items(progress: dict) -> list[dict]:
    grammar = progress.get("grammar", {})
    vocab = progress.get("vocab", {})

    items = []
    for level in ("5", "4", "3", "2", "1"):
        g_started, g_mastered, g_total = _progress(grammar.get(level, {}))
        v_started, v_mastered, v_total = _progress(vocab.get(level, {}))
        subtitle = (
            f"Grammar {g_started}/{g_total} (mastered {g_mastered}) · "
            f"Vocab {v_started}/{v_total} (mastered {v_mastered})"
        )
        items.append(
            item(
                title=bold(f"N{level}"),
                subtitle=subtitle,
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
        progress = get_jlpt_progress(token)
    except BunproError as error:
        emit([error_item(str(error))])
        return

    emit(build_items(progress))


if __name__ == "__main__":
    sys.exit(main())
