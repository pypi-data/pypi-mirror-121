# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clever_config']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'attributedict>=0.3.0,<0.4.0']

setup_kwargs = {
    'name': 'clever-config',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Andrey A. Osipov',
    'author_email': 'developer.osipov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
