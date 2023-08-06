# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyictacp']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyictacp',
    'version': '0.1.1',
    'description': 'ICT Protege Automation and Control Protocol wrapper',
    'long_description': None,
    'author': 'Thomas Hobson',
    'author_email': 'git@hexf.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
