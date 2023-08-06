# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['twiq']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'twiq',
    'version': '0.0.0',
    'description': '',
    'long_description': None,
    'author': 'Manuel Šarić',
    'author_email': 'manuel.saric@2iqresearch.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
