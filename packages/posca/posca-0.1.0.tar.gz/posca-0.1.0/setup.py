# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['posca']

package_data = \
{'': ['*']}

install_requires = \
['pyfiglet>=0.8.post1,<0.9', 'typer[all]>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['posca = posca.main:app']}

setup_kwargs = {
    'name': 'posca',
    'version': '0.1.0',
    'description': 'a tiny portscanning app',
    'long_description': '# POSCA\n\nJust a tiny port scanning cli app',
    'author': 'Leo B.',
    'author_email': 'bernerdoodle@outlook.de',
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
