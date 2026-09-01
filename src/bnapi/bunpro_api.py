"""Minimal BunPro Frontend API client (stdlib only, no third-party deps).

Uses the personal API token flow BunPro added as a stop-gap for the
frontend_api_token cookie's 2-week expiry: append
?dangerously_authenticate_using_api_token=true and pass the token from
Settings > API as a Bearer header.
"""

import http
import json
import urllib.error
import urllib.parse
import urllib.request

from cache import cached

API_BASE = "https://api.bunpro.jp/api/frontend"
ONE_HOUR = 3600
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)


class BunproError(Exception):
    """Raised for any BunPro API failure."""


class BunproAuthError(BunproError):
    """Raised when the API token is missing or rejected (401)."""


def _get(path: str, token: str) -> dict:
    params = {"dangerously_authenticate_using_api_token": "true"}
    url = f"{API_BASE}{path}?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        if error.code == http.HTTPStatus.UNAUTHORIZED:
            raise BunproAuthError("Invalid or missing BunPro API token") from error
        raise BunproError(f"BunPro API returned HTTP {error.code}") from error
    except urllib.error.URLError as error:
        raise BunproError(f"Could not reach BunPro API: {error.reason}") from error


def get_user(token: str, ttl_seconds: int = ONE_HOUR) -> dict:
    """Fetch GET /user and return the flattened user attributes."""
    return cached(f"{API_BASE}/user", ttl_seconds, lambda: _get("/user", token))[
        "user"
    ]["data"]["attributes"]


def get_due(token: str, ttl_seconds: int = ONE_HOUR) -> dict:
    """Fetch GET /user/due: {total_due_grammar, total_due_vocab}."""
    return cached(f"{API_BASE}/user/due", ttl_seconds, lambda: _get("/user/due", token))


def get_base_stats(token: str, ttl_seconds: int = ONE_HOUR) -> dict:
    """Fetch GET /user_stats/base_stats and return the `facts` object."""
    return cached(
        f"{API_BASE}/user_stats/base_stats",
        ttl_seconds,
        lambda: _get("/user_stats/base_stats", token),
    )["facts"]


def get_srs_level_overview(token: str, ttl_seconds: int = ONE_HOUR) -> dict:
    """Fetch GET /user_stats/srs_level_overview: {grammar: {...}, vocab: {...}}."""
    return cached(
        f"{API_BASE}/user_stats/srs_level_overview",
        ttl_seconds,
        lambda: _get("/user_stats/srs_level_overview", token),
    )


def get_jlpt_progress(token: str, ttl_seconds: int = ONE_HOUR) -> dict:
    """Fetch GET /user_stats/jlpt_progress_mixed: {grammar: {...}, vocab: {...}}."""
    return cached(
        f"{API_BASE}/user_stats/jlpt_progress_mixed",
        ttl_seconds,
        lambda: _get("/user_stats/jlpt_progress_mixed", token),
    )


def get_forecast_daily(token: str, ttl_seconds: int = ONE_HOUR) -> dict:
    """Fetch GET /user_stats/forecast_daily: {grammar: {...}, vocab: {...}}."""
    return cached(
        f"{API_BASE}/user_stats/forecast_daily",
        ttl_seconds,
        lambda: _get("/user_stats/forecast_daily", token),
    )


def get_ghost_leeches(token: str, ttl_seconds: int = ONE_HOUR) -> dict:
    """Fetch GET /user_stats/srs_ghost_level_details and return `reviews`."""
    return cached(
        f"{API_BASE}/user_stats/srs_ghost_level_details",
        ttl_seconds,
        lambda: _get("/user_stats/srs_ghost_level_details", token),
    )["reviews"]
