# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tor_project']

package_data = \
{'': ['*']}

install_requires = \
['Automat>=20.2.0,<21.0.0',
 'Twisted>=21.7.0,<22.0.0',
 'bs4>=0.0.1,<0.0.2',
 'cryptography>=3.4.8,<4.0.0',
 'incremental>=21.3.0,<22.0.0',
 'ipaddress>=1.0.23,<2.0.0',
 'lxml>=4.6.3,<5.0.0',
 'pygeoip>=0.3.2,<0.4.0',
 'requests[socks]>=2.26.0,<3.0.0',
 'txtorcon>=21.1.0,<22.0.0',
 'zope.interface>=5.4.0,<6.0.0']

setup_kwargs = {
    'name': 'tor-project',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Ivan Yastrebov',
    'author_email': 'easy.-quest@mail.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
