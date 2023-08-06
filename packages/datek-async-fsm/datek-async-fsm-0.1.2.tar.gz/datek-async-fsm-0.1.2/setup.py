# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datek_async_fsm']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'datek-async-fsm',
    'version': '0.1.2',
    'description': 'Asynchronous Finite State Machine',
    'long_description': '[![pipeline status](https://gitlab.com/DAtek/datek-async-fsm/badges/master/pipeline.svg)](https://gitlab.com/DAtek/datek-async-fsm/-/commits/master)\n[![coverage report](https://gitlab.com/DAtek/datek-async-fsm/badges/master/coverage.svg)](https://gitlab.com/DAtek/datek-async-fsm/-/commits/master)\n\n# Asynchronous Finite State Machine\nFor an example see [`tests/example.py`](https://gitlab.com/DAtek/datek-async-fsm/-/blob/master/tests/example.py)',
    'author': 'Attila Dudas',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/DAtek/datek-async-fsm/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
