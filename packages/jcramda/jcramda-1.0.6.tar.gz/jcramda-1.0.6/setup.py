# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jcramda', 'jcramda.base', 'jcramda.core', 'jcramda.factor']

package_data = \
{'': ['*']}

install_requires = \
['more-itertools>=8.10.0,<9.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'pytz>=2021.1,<2022.0']

setup_kwargs = {
    'name': 'jcramda',
    'version': '1.0.6',
    'description': 'functional programming tools in python',
    'long_description': None,
    'author': 'Jochen.He',
    'author_email': 'thjl@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
