# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datek_async_fsm']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'datek-async-fsm',
    'version': '0.1.1',
    'description': 'Asynchronous Finite State Machine',
    'long_description': None,
    'author': 'Attila Dudas',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
