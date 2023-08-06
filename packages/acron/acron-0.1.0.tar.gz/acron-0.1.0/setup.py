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
    'version': '0.1.0',
    'description': 'Lightweight scheduler',
    'long_description': None,
    'author': 'Thomas Cellerier',
    'author_email': 'thomas.cellerier@appgate.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
