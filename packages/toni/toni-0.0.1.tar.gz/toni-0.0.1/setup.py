# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['toni']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'toni',
    'version': '0.0.1',
    'description': 'A static site generator written in Python.',
    'long_description': '# Toni\n\nA static site generator written in Python.\n',
    'author': 'vcokltfre',
    'author_email': 'vcokltfre@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vcokltfre/toni',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
