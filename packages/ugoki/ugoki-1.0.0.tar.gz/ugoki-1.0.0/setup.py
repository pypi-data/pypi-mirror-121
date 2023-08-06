# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ugoki']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.25,<2.0.0',
 'fastapi>=0.68.1,<0.69.0',
 'pydantic>=1.8.2,<2.0.0',
 'python-multipart>=0.0.5,<0.0.6',
 'uvicorn[standard]>=0.15.0,<0.16.0']

entry_points = \
{'console_scripts': ['ugoki-dev = ugoki.cli:dev',
                     'ugoki-prod = ugoki.cli:prod']}

setup_kwargs = {
    'name': 'ugoki',
    'version': '1.0.0',
    'description': 'API Server to serve random gifs with support for public suggestions',
    'long_description': '# Ugoki API Server\n\nUgoki is a simple server for storing categorized gifs where anyone can suggest\ngifs but the owner can approve them only.\n\n## Usage\n\n### Production\n\nTo install the last stable version, simply run\n\n```\n$ pip install ugoki\n```\n\nTo start a ugoki API server, run `ugoki-prod` with correct arguments.\n\n```\n$ ugoki-prod -h\nusage: ugoki-prod [-h] [-p PORT] [-H HOST] STORAGE SERVE_ROOT AUTH_USER AUTH_PASSWORD DB_STRING\n\npositional arguments:\n  STORAGE               Path to store gifs\n  SERVE_ROOT            Root where the gifs are served by the web server\n  AUTH_USER             Username for API\n  AUTH_PASSWORD         Password for API\n  DB_STRING             String to connect to database. (e.g. sqlite:///ugoki.sqlite)\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -p PORT, --port PORT  Port to listen on. Default: 8000\n  -H HOST, --host HOST  Host to listen for. Default: 127.0.0.1\n```\n\n### Development\n\n- `git clone https://gitlab.com/ceda_ei/ugoki.git/`\n- `cd ugoki`\n- `poetry install`\n- `poetry shell`\n- `ugoki-dev`\n',
    'author': 'Ceda EI',
    'author_email': 'ceda_ei@webionite.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/ceda_ei/ugoki.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
