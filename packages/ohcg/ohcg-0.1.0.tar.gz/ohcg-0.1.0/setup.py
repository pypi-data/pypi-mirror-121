# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ohcg']

package_data = \
{'': ['*'], 'ohcg': ['templates/*']}

install_requires = \
['httpx>=0.19.0,<0.20.0',
 'jinja2>=3.0.1,<4.0.0',
 'pydantic[email]>=1.8.2,<2.0.0',
 'pydash>=5.0.2,<6.0.0',
 'typer[all]>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['ohcg = ohcg.main:app']}

setup_kwargs = {
    'name': 'ohcg',
    'version': '0.1.0',
    'description': 'OpenAPI3 HTTP client generator',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
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
