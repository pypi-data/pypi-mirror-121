# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sonicos_api']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'sonicos-api',
    'version': '0.1.1',
    'description': "Lib to communicate with SonicWall's API",
    'long_description': '============\nSonicOS API\n============\n\n************\nAbout\n************\nThis library provides functions to communicate with SonicWall\'s Firewall API, without the need to build the requests by hand.\n\nIt is built on firmware 6.5.4, compatibility with 7.0.0 should be fine but its yet to be tested.\n\n| Currently only the HTTP Basic login method is supported.\n| If you use HTTPS, it is secure enough ;)\n\n***********\nExamples\n***********\n| ``fwLogin("https://192.168.1.1", "admin", "password", False)``\n| Logs into the firewall for executing the other functions.\n\n| ``getCFSLists("192.168.1.1", False)``\n| Returns all the Content Filter lists configured in the firewall at 192.168.1.1\n\n******************\nSupported Actions\n******************\n| Currently, this lib is focused on the CFS feature of the firewall, so there\'s a very limited number of functions to other features.\n| I\'m hoping to implement it along the way, feel free to help :)',
    'author': 'joaovmlima',
    'author_email': 'oi.oaoj@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
