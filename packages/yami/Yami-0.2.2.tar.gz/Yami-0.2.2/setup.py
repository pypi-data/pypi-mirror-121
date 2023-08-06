# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yami']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['hikari>=2.0.0.dev102,<3.0.0']

setup_kwargs = {
    'name': 'yami',
    'version': '0.2.2',
    'description': 'A command handler that complements Hikari, a Discord API wrapper written in Python.',
    'long_description': '## Yami\n---\n[![CI](https://github.com/Jonxslays/Yami/actions/workflows/continuous-integration.yml/badge.svg)](https://github.com/Jonxslays/Yami/actions/workflows/continuous-integration.yml)\n\nStill in early development. Not ready for use.\n',
    'author': 'Jonxslays',
    'author_email': 'jon@jonxslays.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Jonxslays/Yami',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
