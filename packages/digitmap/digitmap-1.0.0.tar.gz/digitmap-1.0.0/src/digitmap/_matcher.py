# pylint: disable=missing-module-docstring

import re
from typing import NamedTuple
from typing import Sequence

from ._translator import translate


class DigitMapResult(NamedTuple):
    """
    Result of attempting to match a string of dialing inputs to a digit map.
    """

    full_matches: Sequence[str]
    """
    Sequence of digit map strings that were found to fully match the dial string.
    """

    partial_matches: Sequence[str]
    """
    Sequence of digit map strings that were found to partially match the dial string.
    """


def match(expr: str, dial_str: str) -> DigitMapResult:
    """
    Attempts to match a string of dialing input symbols to a digit map.

    If at least one digit map string matches the dial string, a `DigitMapResult` object wil be
    returned. Otherwise, if no matches could be made, the function returns `None`.
    """

    string_patterns = translate(expr)

    full_matches = []
    partial_matches = []
    for string, pattern in string_patterns:
        pattern_match = re.fullmatch(pattern, dial_str)

        if not pattern_match:
            continue

        if None in pattern_match.groups():
            partial_matches.append(string)
        else:
            full_matches.append(string)

    if not full_matches and not partial_matches:
        return None

    return DigitMapResult(full_matches, partial_matches)
