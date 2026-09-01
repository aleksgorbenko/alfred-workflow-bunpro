from forecast import build_items


def test_labels_later_and_tomorrow():
    daily = {
        "grammar": {"later": 16, "tomorrow": 14, "2026-09-03": 24},
        "vocab": {"later": 0, "tomorrow": 3, "2026-09-03": 1},
    }

    items = build_items(daily)

    assert items[0]["title"] == "Later today"
    assert items[0]["subtitle"] == "Grammar 16, Vocab 0"
    assert items[1]["title"] == "Tomorrow"
    assert items[1]["subtitle"] == "Grammar 14, Vocab 3"


def test_labels_dated_keys_as_weekday():
    daily = {"grammar": {"2026-09-03": 24}, "vocab": {"2026-09-03": 1}}
    items = build_items(daily)
    assert items[0]["title"] == "Thu 03/09"
    assert items[0]["subtitle"] == "Grammar 24, Vocab 1"


def test_missing_vocab_key_defaults_to_zero():
    daily = {"grammar": {"later": 5}, "vocab": {}}
    items = build_items(daily)
    assert items[0]["title"] == "Later today"
    assert items[0]["subtitle"] == "Grammar 5, Vocab 0"
