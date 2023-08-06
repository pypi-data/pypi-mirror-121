# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_argparse', 'pydantic_argparse.cli']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.2,<2.0.0', 'typing-inspect>=0.7.1,<0.8.0']

setup_kwargs = {
    'name': 'pydantic-argparse',
    'version': '0.1.0',
    'description': 'Typed Argument Parsing with Pydantic',
    'long_description': None,
    'author': 'Hayden Richards',
    'author_email': 'SupImDos@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
