"""Helpers for building Alfred Script Filter JSON output."""

import json
import sys

_BOLD_UPPER_A = 0x1D400
_BOLD_DIGIT_0 = 0x1D7CE


def bold(text: str) -> str:
    """Render ASCII uppercase letters/digits as Mathematical Bold Unicode."""
    chars = []
    for ch in text:
        if ch.isascii() and "A" <= ch <= "Z":
            chars.append(chr(_BOLD_UPPER_A + (ord(ch) - ord("A"))))
        elif ch.isascii() and ch.isdigit():
            chars.append(chr(_BOLD_DIGIT_0 + (ord(ch) - ord("0"))))
        else:
            chars.append(ch)
    return "".join(chars)


def item(
    title: str,
    subtitle: str = "",
    arg: str | None = None,
    valid: bool = True,
    icon: str | None = None,
) -> dict:
    result: dict = {"title": title, "subtitle": subtitle, "valid": valid}
    if arg is not None:
        result["arg"] = arg
    if icon is not None:
        result["icon"] = {"path": icon}
    return result


def error_item(message: str) -> dict:
    return item(title=message, valid=False)


def emit(items: list[dict]) -> None:
    json.dump({"items": items}, sys.stdout)
