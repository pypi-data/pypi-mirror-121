# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['csv2gs']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'csv2gs',
    'version': '0.1.0',
    'description': 'Upload CSV to Google Sheets using CLI',
    'long_description': None,
    'author': 'Alexey Kulichevskiy',
    'author_email': 'alex@alexchevsky.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
