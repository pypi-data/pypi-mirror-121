# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['escriptorium_connector']

package_data = \
{'': ['*']}

install_requires = \
['backoff>=1.11.1,<2.0.0',
 'requests>=2.26.0,<3.0.0',
 'websocket-client>=1.2.1,<2.0.0']

setup_kwargs = {
    'name': 'escriptorium-connector',
    'version': '0.0.10',
    'description': 'This simple python package makes it easy to connect to an eScriptorium instance and to work with the data there.',
    'long_description': "[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]\n\n# Escriptorium Connector\n\nThis simple python package makes it easy to connect to escriptorium and work with the data stored there.\n\n## Installation\n\nAnd the obligatory: `pip install escriptorium-connector`\n## Usage\n\nIf you are working on a public repository, you will probably want to store your user credentials in a hidden `.env` file that does not get distributed with your code. This is pretty easy to accomplish with [python-dotenv](https://pypi.org/project/python-dotenv/). You will need to provide the connector with an eScriptorium instance URL, the API URL, your username, and your password (see below).\n\nThe `EscriptoriumConnector` class provides (or will provide) all the methods needed to interact programmatically with the eScriptorium platform.\n\nExample usage:\n\n```python\nfrom escriptorium_connector import EscriptoriumConnector\nimport os\nfrom dotenv import load_dotenv\n\n\nif __name__ == '__main__':\n    load_dotenv()\n    url = str(os.getenv('ESCRIPTORIUM_URL'))\n    api = f'{url}api/'\n    username = str(os.getenv('ESCRIPTORIUM_USERNAME'))\n    password = str(os.getenv('ESCRIPTORIUM_PASSWORD'))\n    escr = EscriptoriumConnector(url, api, username, password)\n    print(escr.get_documents())\n\n```\n\nAnd your `.env` file should have:\n\n```txt\nESCRIPTORIUM_URL=https://www.escriptorium.fr/\nESCRIPTORIUM_USERNAME=your escriptorium username\nESCRIPTORIUM_PASSWORD=your escriptorium password\n```\n\nSee [this Jupyter notebook](./example.ipynb) for a longer introduction to the connector.",
    'author': 'Bronson Brown-deVost',
    'author_email': 'bronsonbdevost@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/sofer_mahir/escriptorium_python_connector',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
