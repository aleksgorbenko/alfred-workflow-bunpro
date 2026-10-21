import json
from pathlib import Path
from typing import Any

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "grammar.json"

REQUIRED_FIELDS = {"title", "subtitle", "arg", "match", "autocomplete", "jp", "level"}
MIN_ITEMS = 900


def load_items() -> list[dict[str, Any]]:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))["items"]


def test_has_enough_grammar_points() -> None:
    items = load_items()
    assert len(items) >= MIN_ITEMS


def test_every_item_has_required_fields() -> None:
    items = load_items()
    for item in items:
        missing = REQUIRED_FIELDS - item.keys()
        assert not missing, f"{item.get('jp')} missing {missing}"


def test_every_item_has_non_empty_title_and_arg() -> None:
    items = load_items()
    for item in items:
        assert item["title"].strip()
        assert item["arg"].startswith("https://bunpro.jp/grammar_points/")


def test_titles_include_a_translation() -> None:
    items = load_items()
    without_translation = [it for it in items if " - " not in it["title"]]
    assert not without_translation


def test_match_field_covers_kana_and_romaji() -> None:
    items = load_items()
    for item in items:
        assert item["jp"] in item["match"]
        if item.get("romaji"):
            assert item["romaji"] in item["match"]


def test_no_duplicate_urls() -> None:
    items = load_items()
    urls = [it["arg"] for it in items]
    assert len(urls) == len(set(urls))
