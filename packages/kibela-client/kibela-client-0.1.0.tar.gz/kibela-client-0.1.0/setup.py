# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kibela_client']

package_data = \
{'': ['*']}

install_requires = \
['gql[all]>=3.0.0a6,<4.0.0', 'pydantic[dotenv]>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'kibela-client',
    'version': '0.1.0',
    'description': '',
    'long_description': '# kibela-client-python\n\nUnofficial Python API client for [Kibela](https://kibe.la/).\n',
    'author': 'chanyou0311',
    'author_email': 'chanyou0311@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chanyou0311/kibela-client-python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
