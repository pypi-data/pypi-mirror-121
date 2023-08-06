# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebug', 'nonebug.models']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-cqhttp>=2.0.0-alpha.15,<3.0.0',
 'nonebot-adapter-ding>=2.0.0-alpha.15,<3.0.0',
 'nonebot-adapter-feishu>=2.0.0-alpha.15,<3.0.0',
 'nonebot-adapter-mirai>=2.0.0-alpha.15,<3.0.0',
 'nonebot2>=2.0.0-alpha.15,<3.0.0']

setup_kwargs = {
    'name': 'nonebug',
    'version': '0.1.0',
    'description': 'nonebot2 test framework',
    'long_description': None,
    'author': 'AkiraXie',
    'author_email': 'l997460364@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
