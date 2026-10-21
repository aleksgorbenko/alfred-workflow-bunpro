import json
from typing import TYPE_CHECKING, Any
from unittest.mock import patch

import forecast
import leeches
import levels
import pytest
import stats
import summary
from bunpro_api import BunproError

if TYPE_CHECKING:
    from collections.abc import Callable
    from types import ModuleType

FETCHERS: dict[ModuleType, tuple[str, ...]] = {
    forecast: ("get_forecast_daily",),
    leeches: ("get_ghost_leeches",),
    levels: ("get_jlpt_progress",),
    stats: ("get_srs_level_overview",),
    summary: ("get_user", "get_due", "get_base_stats"),
}
EMPTY_REPLIES: dict[str, dict[str, Any]] = {
    "get_forecast_daily": {"grammar": {"later": 1}, "vocab": {"later": 0}},
    "get_ghost_leeches": {"data": [], "included": []},
    "get_jlpt_progress": {"grammar": {}, "vocab": {}},
    "get_srs_level_overview": {"grammar": {}, "vocab": {}},
    "get_user": {"level": 1, "xp": 0},
    "get_due": {"total_due_grammar": 0, "total_due_vocab": 0},
    "get_base_stats": {"streak": 0},
}


def titles(capsys: pytest.CaptureFixture[str]) -> list[str]:
    return [row["title"] for row in json.loads(capsys.readouterr().out)["items"]]


def fake_fetcher(
    name: str, reply: Callable[[str], dict[str, Any]]
) -> Callable[..., dict[str, Any]]:
    def fetch(*_args: object, **_kwargs: object) -> dict[str, Any]:
        return reply(name)

    return fetch


def run_with(module: ModuleType, reply: Callable[[str], dict[str, Any]]) -> None:
    patches = [
        patch.object(module, name, side_effect=fake_fetcher(name, reply))
        for name in FETCHERS[module]
    ]
    for active in patches:
        active.start()
    try:
        module.main()
    finally:
        for active in patches:
            active.stop()


@pytest.mark.parametrize("module", list(FETCHERS))
def test_main_without_a_token_asks_for_one(
    module: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.delenv("BUNPRO_API_TOKEN", raising=False)
    module.main()
    assert titles(capsys)[0].startswith("No BunPro API token set")


@pytest.mark.parametrize("module", list(FETCHERS))
def test_main_shows_api_errors(
    module: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setenv("BUNPRO_API_TOKEN", "token")

    def fail(_name: str) -> dict[str, Any]:
        msg = "BunPro API returned HTTP 500"
        raise BunproError(msg)

    run_with(module, fail)
    assert titles(capsys) == ["BunPro API returned HTTP 500"]


@pytest.mark.parametrize("module", list(FETCHERS))
def test_main_emits_rows(
    module: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setenv("BUNPRO_API_TOKEN", "token")
    run_with(module, lambda name: EMPTY_REPLIES[name])
    assert titles(capsys)
