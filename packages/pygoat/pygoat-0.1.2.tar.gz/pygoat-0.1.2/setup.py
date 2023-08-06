# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pygoat', 'pygoat.echo']

package_data = \
{'': ['*']}

install_requires = \
['fire==0.4.0',
 'google-cloud-secret-manager>=2.3.0,<3.0.0',
 'pandas==1.2.3',
 'pyarrow>=3.0.0,<4.0.0',
 'python-dotenv>=0.15.0,<0.16.0']

entry_points = \
{'console_scripts': ['goat = pygoat.main:cli']}

setup_kwargs = {
    'name': 'pygoat',
    'version': '0.1.2',
    'description': 'Goat python module',
    'long_description': '# pygoat\n',
    'author': 'Marcello Pontes',
    'author_email': 'marcello@oncase.com.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/oncase/pygoat.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.x,<3.9',
}


setup(**setup_kwargs)
