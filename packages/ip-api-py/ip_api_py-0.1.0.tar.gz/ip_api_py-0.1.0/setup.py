# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ip_api_py']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7,<2', 'requests>=2.26,<3']

setup_kwargs = {
    'name': 'ip-api-py',
    'version': '0.1.0',
    'description': 'unoffical https://ip-api.com/ python API',
    'long_description': None,
    'author': 'dev',
    'author_email': 'dev@qiyutech.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
