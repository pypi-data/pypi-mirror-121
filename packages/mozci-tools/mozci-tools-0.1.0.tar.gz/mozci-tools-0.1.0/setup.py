# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['citools']

package_data = \
{'': ['*']}

install_requires = \
['cleo>=0.8.1,<0.9.0',
 'mozci>=2.0.3,<3.0.0',
 'python-bugzilla>=3.1.0,<4.0.0',
 'unidiff>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['citools = citools.console:cli']}

setup_kwargs = {
    'name': 'mozci-tools',
    'version': '0.1.0',
    'description': "A suite of high-level commandline tools to assist with Firefox's CI",
    'long_description': None,
    'author': 'Andrew Halberstadt',
    'author_email': 'ahal@mozilla.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
