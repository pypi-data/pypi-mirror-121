# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['digitmap']

package_data = \
{'': ['*']}

install_requires = \
['lark>=0.11.3,<0.12.0']

setup_kwargs = {
    'name': 'digitmap',
    'version': '1.0.0',
    'description': 'Package for working with digit maps - a syntax for indicating the sequence of digits that define a valid and complete dialing attempt by a VoIP telephone user.',
    'long_description': '# digitmap\n\n![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/gdereese/digitmap/CI/main?style=for-the-badge)\n![PyPI](https://img.shields.io/pypi/v/digitmap?style=for-the-badge)\n\nPackage for working with digit maps - a syntax for indicating the sequence of digits that define\na valid and complete dialing attempt by a VoIP telephone user.\n\n## Features\n\n* Parses digit maps into their individual string patterns\n* Constructs digit maps from component objects\n* Processes strings of dial events for matches to a digit map (full and partial)\n\n## Installation\n\n```shell\npip install digitmap\n```\n\n## What are digit maps?\n\nNaturally, VoIP systems must collect digits dialed by a telephone user in order to route their call. Most call agents (i.e. IP phones) support two modes of dialing: on-hook and off-hook dialing. On-hook dialing is when the user dials the desired phone number while the handset is still \'on-hook\', and the phone device sends the digits dialed to the gateway when the user lifts the handset.\n\nDetermining what number was dialed is simple, since the phone interprets lifting the handset as the user completing their dial. However, off-hook dialing - where the user lifts the handset first then dials the digits - is more difficult to handle. Without a discreet action for the user to signal they have finished dialing, deciding what number has been dialed is not as straight-forward.\n\nThe digit map is a mechanism that was proposed in [RFC 3435](https://datatracker.ietf.org/doc/html/rfc3435#section-2.1.5) to help address this problem. Based on the Unix egrep syntax, a digit map is defined using a series of patterns that describe the valid sequences of digits that when transmitted from via the gateway, will result in a successful routing.\n\n## Overview of digit map syntax\n\nFor example, the dial plan for a VoIP system might be defined as follows:\n\n| Dial... | for... |\n| ------- | ------ |\n| 0 | Local operator |\n| 00 | Long distance operator |\n| any 4 digits | Local extensions |\n| 8 + any 7 digits | Local numbers |\n| # + any 7 digits | Shortcut to local numbers at other corporate sites |\n| * + any 2 digits | Star services |\n| 9 + 1 + any 10 digits | Long distance numbers |\n| 9 + 011 + up to 15 digits | International numbers |\n\nThe corresponding digit map for this dial plan would be:\n\n```text\n(0T|00T|[1-7]xxx|8xxxxxxx|#xxxxxxx|*xx|91xxxxxxxxxx|9011x.T)\n```\n\nDigit maps can contain one or more individual strings that each describe one of these such rules. The following elements can be used in defining digit maps, each with their own meaning:\n\n| Element | Description |\n| --------- | ----------- |\n| `0`-`9`, `A`-`D`, `#`, `*` | A single DTMF digit or symbol |\n| `x` | Any DTMF digit (`0`-`9`) |\n| `[1-4]` | Any DTMF digit in the specified range(s). In this example, digits `1`, `2`, `3`, and `4` would be matched. Multiple digits and ranges can be placed between the brackets. |\n| `.` | Zero or more occurrences of the preceeding element |\n| `T` | Timer event from the call agent. This symbol is typically used to indicate that the call agent has timed out waiting for additional digits. |\n\n## Usage\n\n### Parsing a digit map\n\n```python\nimport digitmap as dm\n\n# match any 7-digit number OR any 3-digit number ending in \'11`\nexpr = "(xxxxxxx|x11)"\n\ndigit_map = dm.parse(expr)\n\nprint(repr(digit_map))\n```\n\n**Output:**\n\n```text\nDigitMap([\n    DigitMapString([\n        WildcardElement(),\n        WildcardElement(),\n        WildcardElement(),\n        WildcardElement(),\n        WildcardElement(),\n        WildcardElement(),\n        WildcardElement()\n    ]),\n    DigitMapString([\n        WildcardElement(),\n        DtmfElement("1"),\n        DtmfElement("1")\n    ])\n])\n```\n\n### Constructing a digit map\n\n```python\nimport digitmap as dm\nimport digitmap.model as dm_model\n\n# match any 7-digit number OR any 3-digit number ending in \'11`\ndigit_map = dm_model.DigitMap([\n    dm_model.DigitMapString([\n        dm_model.WildcardElement(),\n        dm_model.WildcardElement(),\n        dm_model.WildcardElement(),\n        dm_model.WildcardElement(),\n        dm_model.WildcardElement(),\n        dm_model.WildcardElement(),\n        dm_model.WildcardElement()\n    ]),\n    dm_model.DigitMapString([\n        dm_model.WildcardElement(),\n        dm_model.DtmfElement("1"),\n        dm_model.DtmfElement("1")\n    ])\n])\n\nprint(str(digit_map))\n```\n\n**Output:**\n\n```text\n(xxxxxxx|x11)\n```\n\n### Processing a string of dial events for matches\n\n```python\nfrom digitmap import match\n\n# match any 7-digit number OR any 3-digit number ending in \'11`\nexpr = "(xxxxxxx|x11)"\n\ndial_str = "411"\n\nresult = match(expr, dial_str)\n\nprint(f"Full matches: {result.full_matches}")\nprint(f"Partial matches: {result.exact_matches}")\n```\n\n***Output:**\n\n```text\nFull matches: [\'x11\']\nPartial matches: [\'xxxxxxx\']\n```\n\n## Support\n\nPlease use the project\'s [Issues page](https://github.com/gdereese/digitmap/issues) to report any issues.\n\n## Contributing\n\n### Installing for development\n\n```shell\npoetry install\n```\n\n### Linting source files\n\n```shell\npoetry run pylint --rcfile .pylintrc src/digitmap\n```\n\n### Running tests\n\n```shell\npoetry run pytest\n```\n\n## License\n\nThis library is licensed under the terms of the [MIT](https://choosealicense.com/licenses/MIT/) license.\n',
    'author': 'Gary DeReese',
    'author_email': 'garydereese@sbcglobal.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gdereese/digitmap',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
