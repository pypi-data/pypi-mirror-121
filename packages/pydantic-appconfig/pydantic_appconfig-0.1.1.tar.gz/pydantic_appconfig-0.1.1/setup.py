# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_appconfig']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'boto3>=1.10.27', 'pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'pydantic-appconfig',
    'version': '0.1.1',
    'description': 'Helper package for using AWS App Config with Pydantic',
    'long_description': None,
    'author': 'Validus Tech Team',
    'author_email': 'techteam@validusrm.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
