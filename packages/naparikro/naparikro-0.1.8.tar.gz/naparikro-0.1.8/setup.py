# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['naparikro', 'naparikro.helpers', 'naparikro.widgets']

package_data = \
{'': ['*']}

install_requires = \
['PyQt5>=5.15.4,<6.0.0',
 'PyQtWebEngine>=5.15.4,<6.0.0',
 'arkitekt>=0.1.18,<0.2.0',
 'mikro>=0.1.18,<0.2.0',
 'napari>=0.4.11,<0.5.0']

entry_points = \
{'console_scripts': ['naparikro = naparikro.run:main']}

setup_kwargs = {
    'name': 'naparikro',
    'version': '0.1.8',
    'description': '',
    'long_description': None,
    'author': 'jhnnsrs',
    'author_email': 'jhnnsrs@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
