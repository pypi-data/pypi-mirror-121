# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['checkcert']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'pyOpenSSL>=21.0.0,<22.0.0']

entry_points = \
{'console_scripts': ['checkcert = checkcert.checkcert:main']}

setup_kwargs = {
    'name': 'checkcert',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Alex Kelly',
    'author_email': 'alex.kelly@franklin.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
