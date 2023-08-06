# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docusign_integration',
 'docusign_integration.api',
 'docusign_integration.models']

package_data = \
{'': ['*']}

install_requires = \
['PyMuPDF>=1.18.19,<2.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'pydash>=5.0.2,<6.0.0',
 'requests-oauthlib>=1.3.0,<2.0.0',
 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'docusign-integration',
    'version': '1.1.0',
    'description': '',
    'long_description': None,
    'author': 'nichmorgan-loft',
    'author_email': 'nich.morgan@loft.com.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
