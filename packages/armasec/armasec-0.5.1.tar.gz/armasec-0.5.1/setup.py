# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['armasec', 'armasec.schemas', 'armasec.token_decoders']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.68.0,<0.69.0',
 'httpx>=0.18.2,<0.19.0',
 'py-buzz>=2.1.3,<3.0.0',
 'python-jose[cryptography]>=3.2.0,<4.0.0',
 'snick>=1.0.0,<2.0.0']

entry_points = \
{'pytest11': ['json_decoder = armasec.pytest_extension']}

setup_kwargs = {
    'name': 'armasec',
    'version': '0.5.1',
    'description': 'Injectable FastAPI auth via OIDC',
    'long_description': None,
    'author': 'OmniVector Solutions',
    'author_email': 'info@omnivector.solutions',
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
