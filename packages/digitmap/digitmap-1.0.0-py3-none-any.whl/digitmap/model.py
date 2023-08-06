# pylint: disable=too-few-public-methods

"""
Object model for representing a digit map and the structure of its constituent pattern strings.
"""

from typing import Sequence
from typing import Union


class Element:
    """
    Base class for elements of a digit map string.
    """


class Digit:
    """
    Represents a single DTMF digit (0-9).
    """

    def __init__(self, value: str):
        if len(value) != 1 or not value.isdigit():
            raise ValueError("value must be a single-character string with a digit 0-9")
        self._value = value

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.value == other.value
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._value!r})"

    def __str__(self) -> str:
        return self._value

    @property
    def value(self) -> str:
        """
        Gets the DTMF digit value.
        """

        return self._value


class DtmfElement(Element):
    """
    Represents a specific DTMF digit or symbol.
    """

    def __init__(self, value: str):
        if len(value) != 1 or value.upper() not in [
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
            "A", "B", "C", "D", "E", "F", "#", "*"
        ]:
            raise ValueError(
                "value must be a single-character string with a digit 0-9, letter A-F, #, or *"
            )
        self._value = value

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.value == other.value
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._value!r})"

    def __str__(self) -> str:
        return self._value

    @property
    def value(self) -> str:
        """
        Gets the DTMF symbol value.
        """

        return self._value


class TimerElement(Element):
    """
    Corresponds to a timer event captured into a dial string. This is typically used to indicate
    that a VoIP gateway has timed out waiting for additional digits to be dialed by the caller.
    """

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return "T"


class WildcardElement(Element):
    """
    Digit map string element that requires a match to any DTMF digit (0-9).
    """

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return "x"


class SubRange():
    """
    Requires a match to fall within a range of DTMF digits.
    """

    def __init__(self, start: Digit = None, end: Digit = None):
        self.end = end
        self.start = start

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.start == other.start and
            self.end == other.end
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.start!r}, {self.end!r})"

    def __str__(self) -> str:
        return f"{self.start!s}-{self.end!s}"


RangeItem = Union[Digit, SubRange]


class RangeElement(Element):
    """
    Digit map string element that requires a match to set of individual DTMF digits, or ranges
    thereof.
    """

    def __init__(self, items: Sequence[RangeItem]):
        self._items = list(items)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.items == other.items
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._items!r})"

    def __str__(self) -> str:
        return f"[{''.join(map(str, self._items))}]"

    @property
    def items(self) -> Sequence[RangeItem]:
        """
        Gets the sequence of items included in the range.
        """

        return self._items


class PositionElement(Element):
    """
    Digit map string element that allows any number of occurrences of another specified element.
    """

    def __init__(self, element: Element = None):
        self.element = element

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.element == other.element
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.element!r})"

    def __str__(self) -> str:
        return f"{self.element!s}."


class DigitMapString:
    """
    Made from one or more elements that indicate what sequence of DTMF digits or symbols that
    correspond to a specific handling path in a VoIP gateway.
    """

    def __init__(self, elements: Sequence[Element]):
        self._elements = list(elements)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.elements == other.elements
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._elements!r})"

    def __str__(self) -> str:
        return ''.join(map(str, self._elements))

    @property
    def elements(self) -> Sequence[Element]:
        """
        Gets the sequence of elements for this digit map string.
        """

        return self._elements


class DigitMap:
    """
    Defines patterns for all the valid dialing inputs that can be handled by a VoIP gateway.
    """

    def __init__(self, strings: Sequence[DigitMapString]):
        self._strings = list(strings)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.strings == other.strings
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._strings!r})"

    def __str__(self) -> str:
        if len(self._strings) == 1:
            return str(self._strings[0])
        return f"({'|'.join(map(str, self._strings))})"

    @property
    def strings(self) -> Sequence[DigitMapString]:
        """
        Gets the sequence of individual digit map strings.
        """

        return self._strings
