# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['acron']

package_data = \
{'': ['*']}

install_requires = \
['croniter>=1.0.15,<2.0.0', 'pytz>=2021.1,<2022.0']

setup_kwargs = {
    'name': 'acron',
    'version': '0.1.2',
    'description': 'Lightweight scheduler',
    'long_description': 'Lightweight scheduler for python asyncio\n\nBased on croniter to support the crontab syntax.\n',
    'author': 'Aitor Iturri',
    'author_email': 'aitor.iturri@appgate.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/appgate/acron',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
