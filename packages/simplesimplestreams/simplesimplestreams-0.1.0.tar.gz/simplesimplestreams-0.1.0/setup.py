# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simplesimplestreams']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'simplesimplestreams',
    'version': '0.1.0',
    'description': 'simple simplestreams client',
    'long_description': '# Simple SimpleStreams\n\nA simple client for LXD SimpleStreams, port of lxc/lxd/shared/simplesreams.go\n\n🚧 Under Development 🚧 \\\nOnly a few APIs are implemented\n\n## Usage\n\n```python\nfrom simplesimplestreams import SimpleStreamsClient\n\nclient = SimpleStreamsClient(url="https://images.linuxcontainers.org")\nimages = client.list_images()\n```\n\n## Development\n\nInstall dependencies with poetry: `poetry install` \\\nRun type check: `poetry run mypy . --strict` \\\nRun tests: `poetry run pytest` \\\nFormat code: `poetry run black .`\n\n## License\n\nApache-2.0\n',
    'author': 'otariidae',
    'author_email': 'otariidae@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/otariidae/simplesimplestreams',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
