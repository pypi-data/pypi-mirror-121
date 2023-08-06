# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gazoo']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['gazoo = gazoo:main']}

setup_kwargs = {
    'name': 'gazoo',
    'version': '0.0.2',
    'description': 'Wrap Minecraft bedrock server to make proper backups.',
    'long_description': '# Gazoo <!-- omit in toc -->\n\nWrap Minecraft Bedrock server to make proper backups.\n\n- [Rationale](#rationale)\n- [Installation](#installation)\n- [Configuration](#configuration)\n- [Usage](#usage)\n- [Similar projects](#similar-projects)\n\n\n## Rationale\n\nThe Minecraft Bedrock server expects input from STDIN in order to perfrom\nbackups properly.  Since no other form of IPC exists, a wrapper is used to\nautomate sending the save commands to the Bedrock server\'s STDIN.  The wrapper\nalso forwards all STDIO transparently, so the wrapper acts as a drop-in\nreplacement.\n\n\n## Installation\n\nGazoo is [published][pypi-gazoo] to the [Python Package Index (PyPI)][pypi-home]\nand can be installed with [pip][pip-home].\n\n```bash\npip install gazoo\n```\n\n\n## Configuration\n\nGazoo writes all its files to a `gazoo` subdirectory in the current working\ndirectory.  Running `gazoo` for the first time will create a `gazoo.cfg` file in\nthe `gazoo` subdirectory, among other setup.  The configuration file is a simple\n[INI-style][wikipedia-ini] file with only a few options:\n\n- `backup_interval`\n  - Time between backups (in seconds)\n  - Default value: `600` (10 minutes)\n- `cleanup_interval`\n  - Time between cleanups (in seconds)\n  - Default value: `86400` (24 hours)\n- `debug`\n  - Whether to output debug information\n  - Default value: `false`\n\n\n## Usage\n\nPlease note:  `gazoo` requires being run in the context of the Bedrock server\nroot directory.  This means you will need to `cd` to the Bedrock server root\ndirectory before calling `gazoo`, or set `PWD`, or something else appropriate\nfor your situation.\n\nBy default (without any additional arguments), `gazoo` wraps the Bedrock server\ntransparently (with all STDIO forwarded).  Saving and cleanup is performed\nautomatically as configured in the `gazoo.cfg` file.\n\nFor convenience, two commands are also provided:  `cleanup`, and `restore`.\n\nThe `cleanup` command simply runs the cleanup portion of the program and then\nexits.  This is useful if there are backups that need to be cleaned up, but you\ndon\'t want to start the Bedrock server.\n\nThe `restore` command restores saves made by gazoo.  If used without any\nadditional arguments, `restore` restores the most recent save.  An integer\nargument can be provided to restore the nth most recent save.  E.g. passing `1`\nrestores the first most recent save (and is equivalent to passing nothing),\npassing `2` restores the second most recent save, etc.  Alternatively, a file\npath to a backup can be specified.\n\n\n## Similar projects\n\n[github.com/debkbanerji/minecraft-bedrock-server][github-debkbanerji-minecraft-bedrock-server]\nmay provide some similar functionality (untested/unvetted).\n\n\n<!-- Links -->\n\n[github-debkbanerji-minecraft-bedrock-server]:\nhttps://github.com/debkbanerji/minecraft-bedrock-server\n"GitHub - debkbanerji/minecraft-bedrock-server"\n\n[pip-home]:\nhttps://pip.pypa.io/en/stable/\n"Home - pip documentation"\n\n\n[pypi-home]:\nhttps://pypi.org/\n"PyPI - The Python Package Index"\n\n[pypi-gazoo]:\nhttps://pypi.org/project/gazoo/\n"gazoo - PyPI"\n\n\n[wikipedia-ini]:\nhttps://en.wikipedia.org/wiki/INI_file\n"INI file - Wikipedia"\n',
    'author': 'John Schroeder',
    'author_email': 'john@schroedernet.software',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/thesmiley1/gazoo',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
