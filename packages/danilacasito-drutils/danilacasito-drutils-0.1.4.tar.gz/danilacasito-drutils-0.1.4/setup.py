# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['danilacasito_drutils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'danilacasito-drutils',
    'version': '0.1.4',
    'description': 'Some Utilities (BETA stage)',
    'long_description': None,
    'author': 'Daniel',
    'author_email': 'danilacasito8@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
