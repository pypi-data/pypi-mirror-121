# pylint: disable=missing-module-docstring

from lark import Lark
from lark import v_args
from lark.visitors import Transformer

from .model import Digit
from .model import DigitMap
from .model import DigitMapString
from .model import DtmfElement
from .model import PositionElement
from .model import RangeElement
from .model import SubRange
from .model import TimerElement
from .model import WildcardElement


@v_args(inline=True)
class _TransformToObject(Transformer):
    # pylint: disable=invalid-name
    # pylint: disable=missing-function-docstring
    # pylint: disable=no-self-use

    def start(self, *strings):
        return DigitMap(
            strings=list(strings)
        )

    def string(self, *elements):
        return DigitMapString(
            elements=list(elements)
        )

    def dtmf(self, token):
        return DtmfElement(token.value)

    def timer(self):
        return TimerElement()

    def wildcard(self):
        return WildcardElement()

    def range(self, *items):
        return RangeElement(
            items=list(items)
        )

    def position(self, element):
        return PositionElement(
            element=element
        )

    def sub_range(self, start, end):
        return SubRange(
            end=end,
            start=start
        )

    def digit(self, value):
        return Digit(value)

    def DIGIT(self, token):
        return token.value


def parse(expr: str) -> DigitMapString:
    """
    Parses a digit map expression into an equivalent object representation.
    """

    parser = Lark.open("digitmap.lark", rel_to=__file__)
    ast = parser.parse(expr)

    model = _TransformToObject().transform(ast)

    return model
