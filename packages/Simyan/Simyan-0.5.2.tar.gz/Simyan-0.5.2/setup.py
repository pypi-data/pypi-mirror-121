# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['Simyan']

package_data = \
{'': ['*']}

install_requires = \
['marshmallow>=3.13.0,<4.0.0',
 'ratelimit>=2.2.1,<3.0.0',
 'requests>=2.26.0,<3.0.0']

extras_require = \
{'docs': ['sphinx-rtd-theme>=1.0.0,<2.0.0', 'sphinxcontrib-napoleon>=0.7,<0.8']}

setup_kwargs = {
    'name': 'simyan',
    'version': '0.5.2',
    'description': 'A Python wrapper for the Comicvine API.',
    'long_description': '# Simyan\n\n[![PyPI - Python](https://img.shields.io/pypi/pyversions/Simyan.svg?logo=PyPI&label=Python-Versions&style=flat-square)](https://pypi.python.org/pypi/Simyan/)\n[![PyPI - Status](https://img.shields.io/pypi/status/Simyan.svg?logo=PyPI&label=Status&style=flat-square)](https://pypi.python.org/pypi/Simyan/)\n[![PyPI - Version](https://img.shields.io/pypi/v/Simyan.svg?logo=PyPI&label=Version&style=flat-square)](https://pypi.python.org/pypi/Simyan/)\n[![PyPI - License](https://img.shields.io/pypi/l/Simyan.svg?logo=PyPI&label=License&style=flat-square)](https://opensource.org/licenses/GPL-3.0)\n\n[![Github - Contributors](https://img.shields.io/github/contributors/Buried-In-Code/Simyan.svg?logo=Github&label=Contributors&style=flat-square)](https://github.com/Buried-In-Code/Simyan/graphs/contributors)\n[![Github Action - Code Analysis](https://img.shields.io/github/workflow/status/Buried-In-Code/Simyan/Code-Analysis?logo=Github-Actions&label=Code-Analysis&style=flat-square)](https://github.com/Buried-In-Code/Simyan/actions/workflows/code-analysis.yaml)\n[![Github Action - Testing](https://img.shields.io/github/workflow/status/Buried-In-Code/Simyan/Testing?logo=Github-Actions&label=Tests&style=flat-square)](https://github.com/Buried-In-Code/Simyan/actions/workflows/testing.yaml)\n\n[![Read the Docs](https://img.shields.io/readthedocs/simyan?label=Read-the-Docs&logo=Read-the-Docs&style=flat-square)](https://simyan.readthedocs.io/en/latest/?badge=latest)\n[![Code Style - Black](https://img.shields.io/badge/Code--Style-Black-000000.svg?style=flat-square)](https://github.com/psf/black)\n\nA [Python](https://www.python.org/) wrapper for the [Comicvine](https://comicvine.gamespot.com/api/) API.\n\n## Installation\n\n### PyPI\n\n```bash\n$ pip3 install -U --user Simyan\n```\n\n## Example Usage\n\n```python\nfrom Simyan import api\n# Your config/secrets\nfrom config import comicvine_api_key\n\nsession = api(api_key=comicvine_api_key)\n\n# Search for Publisher\nresults = session.publisher_list(params={\'filter\': \'name:DC Comics\'})\nfor publisher in results:\n    print(f"{publisher.id} | {publisher.name} - {publisher.site_url}")\n\n# Get details for a Volume\nresult = session.volume(_id=26266)\nprint(result.summary)\n```\n\n*There is a cache option to limit required calls to API*\n\n```python\nfrom Simyan import api, SqliteCache\n# Your config/secrets\nfrom config import comicvine_api_key\n\nsession = api(api_key=comicvine_api_key, cache=SqliteCache())\n\n# Get details for an Issue\nresult = session.issue(_id=189810)\nprint(f"{result.volume.name} #{result.number}")\nprint(result.description)\n```\n\n## Socials\n\nBig thanks to [Mokkari](https://github.com/bpepple/mokkari) for the inspiration and template for this project.\n\n[![Social - Discord](https://img.shields.io/discord/618581423070117932.svg?logo=Discord&label=The-DEV-Environment&style=flat-square&colorB=7289da)](https://discord.gg/nqGMeGg)',
    'author': 'Buried-In-Code',
    'author_email': '6057651+Buried-In-Code@users.noreply.github.com',
    'maintainer': 'Buried-In-Code',
    'maintainer_email': '6057651+Buried-In-Code@users.noreply.github.com',
    'url': 'https://github.com/Buried-In-Code/Simyan',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
