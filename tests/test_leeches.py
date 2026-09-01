import datetime as dt

from leeches import build_items

NOW = dt.datetime(2026, 9, 1, 12, 0, tzinfo=dt.UTC)


def _reviews(entries: list[dict]) -> dict:
    data = []
    included = []
    for entry in entries:
        data.append(
            {
                "id": entry["id"],
                "type": "ghost_review",
                "attributes": {
                    "reviewable_id": entry["reviewable_id"],
                    "streak": entry["streak"],
                    "is_slain": entry["is_slain"],
                    "next_review": entry["next_review"],
                },
                "relationships": {
                    "reviewable": {
                        "data": {
                            "type": "reviewable_base_attribute_mixed",
                            "id": entry["reviewable_id"],
                        }
                    }
                },
            }
        )
        included.append(
            {
                "id": entry["reviewable_id"],
                "type": "reviewable_base_attribute_mixed",
                "attributes": {"title": entry["title"], "meaning": entry["meaning"]},
            }
        )
    return {"data": data, "included": included}


def test_shows_active_leech_with_streak_and_next_review():
    reviews = _reviews(
        [
            {
                "id": "1",
                "reviewable_id": "48",
                "streak": 1,
                "is_slain": False,
                "next_review": "2026-09-01T13:00:00.000Z",
                "title": "Verb + にいく",
                "meaning": "To go ~",
            }
        ]
    )

    items = build_items(reviews, NOW)

    assert items[0]["title"] == "Verb + にいく - To go ~"
    assert items[0]["subtitle"] == "streak 1 · next review in 1h"


def test_filters_out_slain_reviews():
    reviews = _reviews(
        [
            {
                "id": "1",
                "reviewable_id": "48",
                "streak": 3,
                "is_slain": True,
                "next_review": "2026-09-01T13:00:00.000Z",
                "title": "Verb + にいく",
                "meaning": "To go ~",
            }
        ]
    )

    items = build_items(reviews, NOW)

    assert items[0]["title"] == "🎉 No leeches - clean SRS!"
    assert items[0]["valid"] is False


def test_no_leeches_when_empty():
    items = build_items({"data": [], "included": []}, NOW)
    assert items[0]["title"] == "🎉 No leeches - clean SRS!"


def test_sorts_by_streak_ascending():
    reviews = _reviews(
        [
            {
                "id": "1",
                "reviewable_id": "1",
                "streak": 5,
                "is_slain": False,
                "next_review": "2026-09-01T13:00:00.000Z",
                "title": "High streak",
                "meaning": "x",
            },
            {
                "id": "2",
                "reviewable_id": "2",
                "streak": 0,
                "is_slain": False,
                "next_review": "2026-09-01T13:00:00.000Z",
                "title": "Low streak",
                "meaning": "y",
            },
        ]
    )

    items = build_items(reviews, NOW)

    assert items[0]["title"].startswith("Low streak")
    assert items[1]["title"].startswith("High streak")
