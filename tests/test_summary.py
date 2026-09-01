from summary import build_items


def test_shows_level_xp_due_and_streak():
    user = {"level": 41, "xp": 94760, "next_level_xp": 98900}
    due = {"total_due_grammar": 37, "total_due_vocab": 0}
    base_stats = {"streak": 7, "days_studied": 43}

    items = build_items(user, due, base_stats)

    assert items[0]["title"] == "Level 41"
    assert items[0]["subtitle"] == "94760/98900 XP"
    assert items[1]["title"] == "Grammar due: 37"
    assert items[2]["title"] == "Vocab due: 0"
    assert items[3]["title"] == "Streak: 7d"
    assert items[3]["subtitle"] == "43 days studied total"
