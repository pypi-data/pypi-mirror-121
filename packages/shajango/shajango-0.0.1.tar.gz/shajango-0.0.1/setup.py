# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shajango']

package_data = \
{'': ['*']}

install_requires = \
['importlib_metadata>=3.4.0,<4.0.0']

setup_kwargs = {
    'name': 'shajango',
    'version': '0.0.1',
    'description': '一个基于Django的CMS。',
    'long_description': '# shajango\n\n\n[![PyPI version](https://badge.fury.io/py/shajango.svg)](https://badge.fury.io/py/shajango)\n![versions](https://img.shields.io/pypi/pyversions/shajango.svg)\n[![GitHub license](https://img.shields.io/github/license/mgancita/shajango.svg)](https://github.com/mgancita/shajango/blob/main/LICENSE)\n\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n\n一个基于Django的CMS。\n\n\n- 开源许可: MIT\n- 文档: https://llango.github.io/shajango.\n\n\n## 特征\n\n* TODO\n\n## 制作\n\n\n该包使用 [Cookiecutter](https://github.com/audreyr/cookiecutter) 和 [`llango/cookiecutter-mkdoc-shapackage`](https://github.com/llango/cookiecutter-mkdoc-shapackage/) 项目模版创建。\n',
    'author': 'rontom ai',
    'author_email': 'rontomai@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/llango/shajango',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
