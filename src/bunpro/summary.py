"""Script Filter: BunPro summary (due counts, level, streak)."""

import os
import sys

from alfred_items import emit, error_item, item
from bunpro_api import BunproError, get_base_stats, get_due, get_user

DASHBOARD_URL = "https://bunpro.jp/dashboard"
ICON_LEVEL = "icons/icon_summary_level.png"
ICON_GRAMMAR_DUE = "icons/icon_summary_grammar_due.png"
ICON_VOCAB_DUE = "icons/icon_summary_vocab_due.png"
ICON_STREAK = "icons/icon_summary_streak.png"


def build_items(user: dict, due: dict, base_stats: dict) -> list[dict]:
    level = user.get("level")
    xp = user.get("xp")
    next_level_xp = user.get("next_level_xp")
    streak = base_stats.get("streak", 0)

    return [
        item(
            title=f"Level {level}",
            subtitle=f"{xp}/{next_level_xp} XP",
            arg=DASHBOARD_URL,
            icon=ICON_LEVEL,
        ),
        item(
            title=f"Grammar due: {due.get('total_due_grammar', 0)}",
            subtitle="Open dashboard",
            arg=DASHBOARD_URL,
            icon=ICON_GRAMMAR_DUE,
        ),
        item(
            title=f"Vocab due: {due.get('total_due_vocab', 0)}",
            subtitle="Open dashboard",
            arg=DASHBOARD_URL,
            icon=ICON_VOCAB_DUE,
        ),
        item(
            title=f"Streak: {streak}d",
            subtitle=f"{base_stats.get('days_studied', 0)} days studied total",
            arg=DASHBOARD_URL,
            icon=ICON_STREAK,
        ),
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
        user = get_user(token)
        due = get_due(token)
        base_stats = get_base_stats(token)
    except BunproError as error:
        emit([error_item(str(error))])
        return

    emit(build_items(user, due, base_stats))


if __name__ == "__main__":
    sys.exit(main())
