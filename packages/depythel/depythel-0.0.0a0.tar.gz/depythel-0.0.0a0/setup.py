# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['depythel', 'depythel.macports']

package_data = \
{'': ['*']}

install_requires = \
['beartype>=0.8.1,<0.9.0', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'depythel',
    'version': '0.0.0a0',
    'description': 'Interdependency Visualiser and Dependency Hell scrutiniser',
    'long_description': None,
    'author': 'harens',
    'author_email': 'harensdeveloper@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
