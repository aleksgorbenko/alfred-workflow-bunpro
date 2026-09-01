from levels import build_items


def test_shows_started_and_mastered_per_jlpt_level():
    progress = {
        "grammar": {
            "5": {
                "beginner": 25,
                "adept": 56,
                "seasoned": 51,
                "expert": 0,
                "master": 0,
                "total_count": 132,
            },
        },
        "vocab": {
            "5": {
                "beginner": 0,
                "adept": 0,
                "seasoned": 136,
                "expert": 0,
                "master": 237,
                "total_count": 1100,
            },
        },
    }

    items = build_items(progress)

    n5 = items[0]
    assert n5["title"] == "𝐍𝟓"
    assert n5["subtitle"] == (
        "Grammar 132/132 (mastered 0) · Vocab 373/1100 (mastered 237)"
    )


def test_orders_n5_through_n1():
    progress = {"grammar": {}, "vocab": {}}
    items = build_items(progress)
    assert [item["title"].split(" - ")[0] for item in items] == [
        "𝐍𝟓",
        "𝐍𝟒",
        "𝐍𝟑",
        "𝐍𝟐",
        "𝐍𝟏",
    ]


def test_missing_level_defaults_to_zero():
    items = build_items({"grammar": {}, "vocab": {}})
    assert items[0]["title"] == "𝐍𝟓"
    assert items[0]["subtitle"] == "Grammar 0/0 (mastered 0) · Vocab 0/0 (mastered 0)"
