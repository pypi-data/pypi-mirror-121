# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polundra', 'polundra.audio', 'polundra.visual']

package_data = \
{'': ['*']}

install_requires = \
['Wave>=0.0.2,<0.0.3', 'dbus-python>=1.2.16,<2.0.0', 'pulsectl>=21.9.1,<22.0.0']

setup_kwargs = {
    'name': 'polundra',
    'version': '0.1.0',
    'description': 'An extended alert notifier.',
    'long_description': None,
    'author': 'Artur Svistunov',
    'author_email': 'poopa@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
