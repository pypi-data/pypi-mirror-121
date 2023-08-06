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
    'version': '0.1.3',
    'description': 'Lightweight scheduler',
    'long_description': 'Lightweight scheduler for python asyncio\n\nBased on croniter to support the crontab syntax.\n\n\n.. code:: python\n\n    import asyncio\n\n    from acron.scheduler import Scheduler, Job\n\n    async def do_the_thing():\n        print(\'Doing the thing\')\n\n    async def run_jobs_forever():\n        stop = asyncio.Event()\n\n        do_thing = Job(\n            name="Do the thing",\n            schedule="0/1 * * * *",\n            func=do_the_thing,\n        )\n\n        async with Scheduler() as scheduler:\n            await scheduler.update_jobs({do_thing})\n            await stop.wait()\n\n    if __name__ == \'__main__\':\n        try:\n            asyncio.run(run_jobs_forever())\n        except KeyboardInterrupt:\n            print(\'Bye.\')\n',
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
