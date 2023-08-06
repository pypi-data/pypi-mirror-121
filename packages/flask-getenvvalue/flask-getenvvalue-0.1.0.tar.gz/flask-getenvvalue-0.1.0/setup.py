# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_getenvvalue']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'flask-getenvvalue',
    'version': '0.1.0',
    'description': 'Loading a values from environment variable and set to app.config. ',
    'long_description': None,
    'author': 'Yusuke Ohshima',
    'author_email': 'ohshima.yusuke@yukke.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
