# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_mongodb']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0',
 'fastapi>=0.68.1,<0.69.0',
 'motor>=2.5.1,<3.0.0',
 'pydantic[email,dotenv]>=1.8.2,<2.0.0',
 'pyjwt>=2.1.0,<3.0.0',
 'pymongo[tls,srv]>=3.12.0,<4.0.0']

extras_require = \
{'orjson': ['orjson>=3.6.3,<4.0.0']}

setup_kwargs = {
    'name': 'fastapi-mongodb',
    'version': '0.0.1b4',
    'description': 'A library that simplifies work and integration with MongoDB for a FastAPI project.',
    'long_description': '# FastAPI❤MongoDB\n![GitHub](https://img.shields.io/github/license/Kostiantyn-Salnykov/fastapi-mongodb)\n![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/Kostiantyn-Salnykov/fastapi-mongodb/Python%20package/master)\n![GitHub last commit (branch)](https://img.shields.io/github/last-commit/kostiantyn-salnykov/fastapi-mongodb/master)\n[![codecov](https://codecov.io/gh/Kostiantyn-Salnykov/fastapi-mongodb/branch/master/graph/badge.svg?token=77Z4DQVIU5)](https://codecov.io/gh/Kostiantyn-Salnykov/fastapi-mongodb)\n\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fastapi-mongodb)\n![PyPI](https://img.shields.io/pypi/v/fastapi-mongodb)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/fastapi-mongodb)\n\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n[![](https://img.shields.io/badge/code%20style-black-000000?style=flat)](https://github.com/psf/black)\n\n# Installation\n\n```shell\npip install fastapi-mongodb\n```\n\n# FastAPI❤MongoDB documentation:\n\n## [Documentation](https://Kostiantyn-Salnykov.github.io/fastapi-mongodb/)\n',
    'author': 'Kostiantyn Salnykov',
    'author_email': 'kostiantyn.salnykov@gmail.com',
    'maintainer': 'Kostiantyn Salnykov',
    'maintainer_email': 'kostiantyn.salnykov@gmail.com',
    'url': 'https://kostiantyn-salnykov.github.io/fastapi-mongodb/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
