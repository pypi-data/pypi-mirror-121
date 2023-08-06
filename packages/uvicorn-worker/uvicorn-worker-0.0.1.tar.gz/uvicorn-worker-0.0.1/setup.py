# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uvicorn_worker']

package_data = \
{'': ['*']}

install_requires = \
['gunicorn>=20.1.0', 'uvicorn>=0.12.0']

setup_kwargs = {
    'name': 'uvicorn-worker',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Marcelo Trylesinski',
    'author_email': 'marcelotryle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
