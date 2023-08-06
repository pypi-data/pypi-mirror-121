# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['countdown_sleep']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['countdown_sleep = countdown_sleep.main:cli']}

setup_kwargs = {
    'name': 'countdown-sleep',
    'version': '0.1.1',
    'description': 'Sleep and print countdown.',
    'long_description': '# countdown-sleep\n\nSleep and print countdown.\n\n## Installation\n\n```\n$ pip install countdown-sleep\n```\n\n## Usage\n\n```\n$ countdown_sleep --help\nusage: countdown_sleep [-h] second\n\nSleep and print countdown.\n\npositional arguments:\n  second      sleep seconds\n\noptional arguments:\n  -h, --help  show this help message and exit\n```\n\n```\n$ countdown_sleep 10\n# <sleep and print countdown>\n```\n',
    'author': 'chanyou0311',
    'author_email': 'chanyou0311@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chanyou0311/countdown-sleep',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
