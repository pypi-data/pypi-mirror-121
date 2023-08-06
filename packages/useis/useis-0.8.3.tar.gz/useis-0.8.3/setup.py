# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['useis',
 'useis.clients',
 'useis.clients.old_api_client',
 'useis.core',
 'useis.processors',
 'useis.sandbox',
 'useis.services',
 'useis.services.grid_service',
 'useis.services.models',
 'useis.settings']

package_data = \
{'': ['*'],
 'useis.services': ['projects/test/TN/config/*',
                    'projects/test/TN/templates/*',
                    'projects/test/TN/velocities/*'],
 'useis.services.grid_service': ['test_project/TN/config/*',
                                 'test_project/TN/inventory/*',
                                 'test_project/TN/templates/*',
                                 'test_project/TN/times/*',
                                 'test_project/TN/velocities/*',
                                 'test_project/test_network/config/*',
                                 'test_project/test_network/templates/*']}

install_requires = \
['dynaconf>=3.1.4,<4.0.0',
 'fastapi>=0.68.1,<0.69.0',
 'furl>=2.1.2,<3.0.0',
 'grpcio-tools>=1.39.0,<2.0.0',
 'grpcio>=1.39.0,<2.0.0',
 'myst-parser>=0.15.1,<0.16.0',
 'pydantic>=1.8.2,<2.0.0',
 'python-multipart>=0.0.5,<0.0.6',
 'rinohtype>=0.5.3,<0.6.0',
 'tqdm>=4.59.0,<5.0.0',
 'uquake>=0.8,<0.9',
 'uvicorn>=0.15.0,<0.16.0']

extras_require = \
{':extra == "docs"': ['Sphinx>=4.1.2,<5.0.0', 'sphinx-rtd-theme>=0.5.2,<0.6.0']}

setup_kwargs = {
    'name': 'useis',
    'version': '0.8.3',
    'description': '',
    'long_description': None,
    'author': 'jpmercier',
    'author_email': 'jpmercier01@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
