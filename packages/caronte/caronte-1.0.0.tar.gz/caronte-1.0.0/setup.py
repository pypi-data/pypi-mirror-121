# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['caronte', 'caronte.database']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.23,<2.0.0',
 'psycopg2-binary>=2.9.1,<3.0.0',
 'requests>=2.26.0,<3.0.0',
 'telepot>=12.7,<13.0']

setup_kwargs = {
    'name': 'caronte',
    'version': '1.0.0',
    'description': 'A telegram bot that allows users to access groupchats using authentication.',
    'long_description': None,
    'author': 'Lorenzo Balugani',
    'author_email': 'lorenzo.balugani@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.5,<4.0.0',
}


setup(**setup_kwargs)
