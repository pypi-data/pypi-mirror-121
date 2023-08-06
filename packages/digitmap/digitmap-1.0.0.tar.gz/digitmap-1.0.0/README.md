# digitmap

![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/gdereese/digitmap/CI/main?style=for-the-badge)
![PyPI](https://img.shields.io/pypi/v/digitmap?style=for-the-badge)

Package for working with digit maps - a syntax for indicating the sequence of digits that define
a valid and complete dialing attempt by a VoIP telephone user.

## Features

* Parses digit maps into their individual string patterns
* Constructs digit maps from component objects
* Processes strings of dial events for matches to a digit map (full and partial)

## Installation

```shell
pip install digitmap
```

## What are digit maps?

Naturally, VoIP systems must collect digits dialed by a telephone user in order to route their call. Most call agents (i.e. IP phones) support two modes of dialing: on-hook and off-hook dialing. On-hook dialing is when the user dials the desired phone number while the handset is still 'on-hook', and the phone device sends the digits dialed to the gateway when the user lifts the handset.

Determining what number was dialed is simple, since the phone interprets lifting the handset as the user completing their dial. However, off-hook dialing - where the user lifts the handset first then dials the digits - is more difficult to handle. Without a discreet action for the user to signal they have finished dialing, deciding what number has been dialed is not as straight-forward.

The digit map is a mechanism that was proposed in [RFC 3435](https://datatracker.ietf.org/doc/html/rfc3435#section-2.1.5) to help address this problem. Based on the Unix egrep syntax, a digit map is defined using a series of patterns that describe the valid sequences of digits that when transmitted from via the gateway, will result in a successful routing.

## Overview of digit map syntax

For example, the dial plan for a VoIP system might be defined as follows:

| Dial... | for... |
| ------- | ------ |
| 0 | Local operator |
| 00 | Long distance operator |
| any 4 digits | Local extensions |
| 8 + any 7 digits | Local numbers |
| # + any 7 digits | Shortcut to local numbers at other corporate sites |
| * + any 2 digits | Star services |
| 9 + 1 + any 10 digits | Long distance numbers |
| 9 + 011 + up to 15 digits | International numbers |

The corresponding digit map for this dial plan would be:

```text
(0T|00T|[1-7]xxx|8xxxxxxx|#xxxxxxx|*xx|91xxxxxxxxxx|9011x.T)
```

Digit maps can contain one or more individual strings that each describe one of these such rules. The following elements can be used in defining digit maps, each with their own meaning:

| Element | Description |
| --------- | ----------- |
| `0`-`9`, `A`-`D`, `#`, `*` | A single DTMF digit or symbol |
| `x` | Any DTMF digit (`0`-`9`) |
| `[1-4]` | Any DTMF digit in the specified range(s). In this example, digits `1`, `2`, `3`, and `4` would be matched. Multiple digits and ranges can be placed between the brackets. |
| `.` | Zero or more occurrences of the preceeding element |
| `T` | Timer event from the call agent. This symbol is typically used to indicate that the call agent has timed out waiting for additional digits. |

## Usage

### Parsing a digit map

```python
import digitmap as dm

# match any 7-digit number OR any 3-digit number ending in '11`
expr = "(xxxxxxx|x11)"

digit_map = dm.parse(expr)

print(repr(digit_map))
```

**Output:**

```text
DigitMap([
    DigitMapString([
        WildcardElement(),
        WildcardElement(),
        WildcardElement(),
        WildcardElement(),
        WildcardElement(),
        WildcardElement(),
        WildcardElement()
    ]),
    DigitMapString([
        WildcardElement(),
        DtmfElement("1"),
        DtmfElement("1")
    ])
])
```

### Constructing a digit map

```python
import digitmap as dm
import digitmap.model as dm_model

# match any 7-digit number OR any 3-digit number ending in '11`
digit_map = dm_model.DigitMap([
    dm_model.DigitMapString([
        dm_model.WildcardElement(),
        dm_model.WildcardElement(),
        dm_model.WildcardElement(),
        dm_model.WildcardElement(),
        dm_model.WildcardElement(),
        dm_model.WildcardElement(),
        dm_model.WildcardElement()
    ]),
    dm_model.DigitMapString([
        dm_model.WildcardElement(),
        dm_model.DtmfElement("1"),
        dm_model.DtmfElement("1")
    ])
])

print(str(digit_map))
```

**Output:**

```text
(xxxxxxx|x11)
```

### Processing a string of dial events for matches

```python
from digitmap import match

# match any 7-digit number OR any 3-digit number ending in '11`
expr = "(xxxxxxx|x11)"

dial_str = "411"

result = match(expr, dial_str)

print(f"Full matches: {result.full_matches}")
print(f"Partial matches: {result.exact_matches}")
```

***Output:**

```text
Full matches: ['x11']
Partial matches: ['xxxxxxx']
```

## Support

Please use the project's [Issues page](https://github.com/gdereese/digitmap/issues) to report any issues.

## Contributing

### Installing for development

```shell
poetry install
```

### Linting source files

```shell
poetry run pylint --rcfile .pylintrc src/digitmap
```

### Running tests

```shell
poetry run pytest
```

## License

This library is licensed under the terms of the [MIT](https://choosealicense.com/licenses/MIT/) license.
