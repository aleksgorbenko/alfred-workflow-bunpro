import json
import time
from typing import TYPE_CHECKING
from unittest.mock import MagicMock, patch

import forecast
import leeches
import levels
import stats
import summary
from app import PAGES
from pages import PageCache
from workflow import LOADERS, code_version, main, spawn_refresh

if TYPE_CHECKING:
    import pytest


def test_every_page_has_a_loader() -> None:
    assert set(LOADERS) == set(PAGES)


def test_main_prints_menu(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.delenv("BUNPRO_API_TOKEN", raising=False)
    main([])
    assert len(json.loads(capsys.readouterr().out)["items"]) == len(PAGES)


def _one_row(_token: str) -> list[dict[str, str]]:
    return [{"title": "大"}]


def test_main_refresh_stores_page(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BUNPRO_API_TOKEN", "token")
    monkeypatch.setitem(LOADERS, "summary", _one_row)
    main(["--refresh", "summary"])
    hit = PageCache(time.time, code_version()).read("summary", 60)
    assert hit is not None
    assert hit.data == {"rows": [{"title": "大"}]}


@patch("subprocess.Popen")
def test_spawn_refresh_runs_detached(popen: MagicMock) -> None:
    spawn_refresh("summary")
    command = popen.call_args.args[0]
    assert command[-2:] == ["--refresh", "summary"]
    assert popen.call_args.kwargs["start_new_session"] is True


@patch("summary.get_base_stats", return_value={"streak": 4})
@patch("summary.get_due", return_value={"total_due_grammar": 2})
@patch("summary.get_user", return_value={"level": 7, "xp": 1, "next_level_xp": 9})
def test_summary_load(*_mocks: MagicMock) -> None:
    assert [row["title"] for row in summary.load("token")] == [
        "Level 7",
        "Grammar due: 2",
        "Vocab due: 0",
        "Streak: 4d",
    ]


@patch("stats.get_srs_level_overview", return_value={"grammar": {"master": 2}})
def test_stats_load(*_mocks: MagicMock) -> None:
    assert stats.load("token")[-1]["title"] == "Master: 2"


@patch("levels.get_jlpt_progress", return_value={})
def test_levels_load(*_mocks: MagicMock) -> None:
    assert len(levels.load("token")) == len(("5", "4", "3", "2", "1"))


@patch("forecast.get_forecast_daily", return_value={"grammar": {"later": 1}})
def test_forecast_load(*_mocks: MagicMock) -> None:
    assert forecast.load("token")[0]["title"] == "Later today"


@patch("leeches.get_ghost_leeches", return_value={"data": [], "included": []})
def test_leeches_load(*_mocks: MagicMock) -> None:
    assert leeches.load("token")[0]["valid"] is False
