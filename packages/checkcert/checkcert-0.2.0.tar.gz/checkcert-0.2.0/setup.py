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
    'version': '0.2.0',
    'description': 'CLI to check tls cert information and determine validity',
    'long_description': '# checkcert\n\nThis utility was based off of [this\ngist](https://gist.github.com/gdamjan/55a8b9eec6cf7b771f92021d93b87b2c).\n\nI have wrapped the logic in a click-based CLI and added command-line options\n(checkcert --help to see them)\n\n# Installation\n\n## from PyPi\npip install checkert\n\n',
    'author': 'Alex Kelly',
    'author_email': 'kellya@arachnitech.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kellya/checkcert',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
