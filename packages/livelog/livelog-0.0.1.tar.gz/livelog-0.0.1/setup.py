# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['livelog']

package_data = \
{'': ['*']}

install_requires = \
['colorama==0.4.4', 'pynput==1.7.3', 'watchdog==2.1.5']

setup_kwargs = {
    'name': 'livelog',
    'version': '0.0.1',
    'description': 'File logger and live reader',
    'long_description': '# livelog\n\nWork in progress\n',
    'author': 'PabloLec',
    'author_email': 'pablo.lecolinet@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PabloLec/livelog',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
