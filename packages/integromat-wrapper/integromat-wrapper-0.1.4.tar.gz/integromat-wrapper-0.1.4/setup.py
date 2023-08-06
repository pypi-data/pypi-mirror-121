# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['integromat_wrapper']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'httpx>=0.19.0,<0.20.0', 'taskipy>=1.8.2,<2.0.0']

entry_points = \
{'console_scripts': ['integromat-deploy = integromat_wrapper.deploy:deploy']}

setup_kwargs = {
    'name': 'integromat-wrapper',
    'version': '0.1.4',
    'description': '',
    'long_description': None,
    'author': 'Skyler Lewis',
    'author_email': 'skyler@hivewire.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
