# pylint: disable=missing-module-docstring

from functools import reduce
from re import escape
from typing import Iterable

from lark import Lark
from lark import v_args
from lark.visitors import Transformer


@v_args(inline=True)
class _TranslateToRegex(Transformer):
    # pylint: disable=invalid-name
    # pylint: disable=missing-function-docstring
    # pylint: disable=no-self-use

    def __init__(self, expr: str, visit_tokens: bool = None):
        super().__init__(visit_tokens=visit_tokens)

        self._expr = expr

    def start(self, *strings):
        return list(strings)

    @v_args(inline=True, meta=True)
    def string(self, meta, *elements):
        orig_expr = self._expr[meta.start_pos:meta.end_pos]

        # nest each element into an optional group so the pattern will match partial
        string_obj = reduce(lambda p, e: f"({e}{p})?", reversed(elements), "").rstrip("?")

        return (orig_expr, string_obj)

    def dtmf(self, token):
        return escape(token.value)

    def wildcard(self):
        return r"\d"

    def timer(self):
        return "T"

    def range(self, *items):
        return f"[{''.join(items)}]"

    def position(self, element):
        return f"{element}*?"

    def sub_range(self, start, end):
        return f"{start}-{end}"

    def digit(self, token):
        return token.value

    def DIGIT(self, token):
        return token.value


def translate(expr: str) -> Iterable[str]:
    """
    Translates a digit map expression to an equivalent list of regular expressions. These regular
    expressions are used to perform the actual logic for matching digit maps.
    """

    parser = Lark.open("digitmap.lark", propagate_positions=True, rel_to=__file__)
    ast = parser.parse(expr)

    patterns = _TranslateToRegex(expr).transform(ast)

    return patterns
