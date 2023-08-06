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
    'version': '0.0.0',
    'description': '一基于Django的管理系统',
    'long_description': '# shajango\n\n\n[![PyPI version](https://badge.fury.io/py/shajango.svg)](https://badge.fury.io/py/shajango)\n![versions](https://img.shields.io/pypi/pyversions/shajango.svg)\n[![GitHub license](https://img.shields.io/github/license/mgancita/shajango.svg)](https://github.com/mgancita/shajango/blob/main/LICENSE)\n\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n\n一基于Django的管理系统\n\n\n- Free software: MIT\n- Documentation: https://llango.github.io/shajango.\n\n\n## Features\n\n* TODO\n\n## Credits\n\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [`llango/cookiecutter-mkdoc-shapackage`](https://github.com/llango/cookiecutter-mkdoc-shapackage/) project template.\n',
    'author': 'Rontomai',
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
