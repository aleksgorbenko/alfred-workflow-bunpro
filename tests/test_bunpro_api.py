import urllib.error
from unittest.mock import patch

import pytest
from bunpro_api import (
    BunproAuthError,
    get_base_stats,
    get_due,
    get_forecast_daily,
    get_ghost_leeches,
    get_jlpt_progress,
    get_srs_level_overview,
    get_user,
)


@patch("bunpro_api.urllib.request.urlopen")
def test_get_user_returns_flattened_attributes(mock_urlopen):
    payload = {"user": {"data": {"attributes": {"level": 41, "xp": 94760}}}}
    with patch("bunpro_api.json.load", return_value=payload):
        result = get_user("token")
    assert result == {"level": 41, "xp": 94760}
    assert mock_urlopen.called


@patch("bunpro_api.urllib.request.urlopen")
def test_get_user_sends_auth_header_and_dangerous_flag(mock_urlopen):
    payload = {"user": {"data": {"attributes": {}}}}
    with patch("bunpro_api.json.load", return_value=payload):
        get_user("secret-token")

    request = mock_urlopen.call_args[0][0]
    assert request.get_header("Authorization") == "Bearer secret-token"
    assert "dangerously_authenticate_using_api_token=true" in request.full_url


@patch("bunpro_api.urllib.request.urlopen")
def test_get_due_returns_body_as_is(mock_urlopen):
    payload = {"total_due_grammar": 37, "total_due_vocab": 0}
    with patch("bunpro_api.json.load", return_value=payload):
        result = get_due("token")
    assert result == payload
    assert mock_urlopen.called


@patch("bunpro_api.urllib.request.urlopen")
def test_get_base_stats_returns_facts_object(mock_urlopen):
    payload = {"facts": {"streak": 7}, "badges": {"data": []}}
    with patch("bunpro_api.json.load", return_value=payload):
        result = get_base_stats("token")
    assert result == {"streak": 7}
    assert mock_urlopen.called


@patch("bunpro_api.urllib.request.urlopen")
def test_get_srs_level_overview_returns_body_as_is(mock_urlopen):
    payload = {"grammar": {}, "vocab": {}}
    with patch("bunpro_api.json.load", return_value=payload):
        result = get_srs_level_overview("token")
    assert result == payload
    assert mock_urlopen.called


@patch("bunpro_api.urllib.request.urlopen")
def test_get_jlpt_progress_returns_body_as_is(mock_urlopen):
    payload = {"grammar": {}, "vocab": {}}
    with patch("bunpro_api.json.load", return_value=payload):
        result = get_jlpt_progress("token")
    assert result == payload
    assert mock_urlopen.called


@patch("bunpro_api.urllib.request.urlopen")
def test_get_forecast_daily_returns_body_as_is(mock_urlopen):
    payload = {"grammar": {"later": 16}, "vocab": {"later": 0}}
    with patch("bunpro_api.json.load", return_value=payload):
        result = get_forecast_daily("token")
    assert result == payload
    assert mock_urlopen.called


@patch("bunpro_api.urllib.request.urlopen")
def test_get_ghost_leeches_returns_reviews_object(mock_urlopen):
    payload = {"type": "ghost", "reviews": {"data": [], "included": []}}
    with patch("bunpro_api.json.load", return_value=payload):
        result = get_ghost_leeches("token")
    assert result == {"data": [], "included": []}
    assert mock_urlopen.called


@patch("bunpro_api.urllib.request.urlopen")
def test_raises_auth_error_on_401(mock_urlopen):
    mock_urlopen.side_effect = urllib.error.HTTPError(
        url="", code=401, msg="Unauthorized", hdrs=None, fp=None
    )
    with pytest.raises(BunproAuthError):
        get_user("bad-token")
