# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['high_order_layers_torch']

package_data = \
{'': ['*']}

install_requires = \
['pytorch-lightning', 'torch']

setup_kwargs = {
    'name': 'high-order-layers-torch',
    'version': '1.0.0',
    'description': 'High order layers in pytorch',
    'long_description': None,
    'author': 'jloverich',
    'author_email': 'john.loverich@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
