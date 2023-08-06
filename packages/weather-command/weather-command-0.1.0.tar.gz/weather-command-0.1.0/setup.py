# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['weather_command', 'weather_command.models']

package_data = \
{'': ['*']}

install_requires = \
['camel-converter[pydantic]>=1.0.2,<2.0.0',
 'httpx>=0.19.0,<0.20.0',
 'mypy>=0.910,<0.911',
 'pydantic>=1.8.2,<2.0.0',
 'python-dotenv>=0.19.0,<0.20.0',
 'rich>=10.11.0,<11.0.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['weather-command = weather_command.__main__:app']}

setup_kwargs = {
    'name': 'weather-command',
    'version': '0.1.0',
    'description': 'Command line weather app',
    'long_description': "# Weather Command\n\n[![Tests Status](https://github.com/sanders41/weather-command/workflows/Testing/badge.svg?branch=main&event=push)](https://github.com/sanders41/weather-command/actions?query=workflow%3ATesting+branch%3Amain+event%3Apush)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/sanders41/weather-command/main.svg)](https://results.pre-commit.ci/latest/github/sanders41/weather-command/main)\n[![Coverage](https://codecov.io/github/sanders41/weather-command/coverage.svg?branch=main)](https://codecov.io/gh/sanders41/weather-command)\n[![PyPI version](https://badge.fury.io/py/weather-command.svg)](https://badge.fury.io/py/weather-command)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/weather-command?color=5cc141)](https://github.com/sanders41/weather-command)\n\nA command line weather app\n\n## Installation\n\nInstallation with [pipx](https://github.com/pypa/pipx) is recommended.\n\n```sh\npipx install weather-command\n```\n\nAlternatively Weather Command can be installed with pip.\n\n```sh\npip install weather-command\n```\n\n## Useage\n\nFirst an API key is needed from [OpenWeather](https://openweathermap.org/), A free account is all that\nis needed. Once you have your API key create an environment variable named `OPEN_WEATHER_API_KEY` that\nconstains your API key.\n\n```sh\nexport OPEN_WEATHER_API_KEY=your-api-key\n```\n\nTo get the weather for a city:\n\n```sh\nweather-command city seattle\n```\n\n### Arguments\n\n* [HOW]: How to get the weather. Accepted values are city and zip. [default: city]\n* [CITY_ZIP]: The name of the city or zip code for which the weather should be retrieved. If the\nfirst argument is 'city' this should be the name of the city, or if 'zip' it should be the zip\ncode. [required]\n\n### Options\n\n* -u, --units: The units to use. Accepted values are metricand imperial. [default: metric]\n* -s, --state-code: The name of the state where the city is located.\n* -c, --country-code: The country code where the city is located.\n* --am-pm: If this flag is set the times will be displayed in 12 hour format, otherwise times\nwill be 24 hour format.\n* -t, --temp-only: If this flag is set only tempatures will be displayed.\n* --terminal_width: Allows for overriding the default terminal width.\n* --install-completion [bash|zsh|fish|powershell|pwsh]: Install completion for the specified shell.\n* --show-completion [bash|zsh|fish|powershell|pwsh]: Show completion for the specified shell, to\ncopy it or customize the installation.\n* --help: Show this message and exit.\n\n## Contributing\n\nContributions to this project are welcome. If you are interesting in contributing please see our [contributing guide](CONTRIBUTING.md)\n",
    'author': 'Paul Sanders',
    'author_email': 'psanders1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sanders41/weather-command',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
