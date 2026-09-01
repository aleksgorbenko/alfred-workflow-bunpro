from stats import build_items


def test_sums_grammar_and_vocab_per_stage():
    overview = {
        "grammar": {
            "beginner": 29,
            "adept": 56,
            "seasoned": 51,
            "expert": 0,
            "master": 0,
        },
        "vocab": {
            "beginner": 0,
            "adept": 0,
            "seasoned": 504,
            "expert": 0,
            "master": 603,
        },
    }

    items = build_items(overview)

    assert items[0]["title"] == "Beginner: 29"
    assert items[0]["subtitle"] == "Grammar 29 · Vocab 0"
    assert items[2]["title"] == "Seasoned: 555"
    assert items[2]["subtitle"] == "Grammar 51 · Vocab 504"
    assert items[4]["title"] == "Master: 603"


def test_missing_stage_keys_default_to_zero():
    items = build_items({"grammar": {}, "vocab": {}})
    assert all(item["title"].endswith(": 0") for item in items)
