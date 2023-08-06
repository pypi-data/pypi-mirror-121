"""
Package for working with digit maps - a syntax for indicating the sequence of digits that define
a valid and complete dialing attempt.

Digit maps are commonly used to define dialing plan rules for a VoIP system.
"""


from ._parser import parse
from ._matcher import match

__all__ = [
    match.__name__,
    parse.__name__
]
