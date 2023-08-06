# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drivy_tools', 'drivy_tools.src']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.19.0,<0.20.0', 'pydantic>=1.8.2,<2.0.0', 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['drivy = drivy_tools.main:main']}

setup_kwargs = {
    'name': 'drivy-tools',
    'version': '0.2.1',
    'description': '',
    'long_description': None,
    'author': 'zekiblue',
    'author_email': 'zekiberkulu@gmail.com',
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
