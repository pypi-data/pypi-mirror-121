# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shachbuildsystemtest']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'shachbuildsystemtest',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Shacham Ginat',
    'author_email': 'shacham.ginat@pagaya.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.5,<4.0.0',
}


setup(**setup_kwargs)
