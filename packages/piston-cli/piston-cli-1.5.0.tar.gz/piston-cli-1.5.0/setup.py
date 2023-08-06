# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['piston',
 'piston.commands',
 'piston.configuration',
 'piston.configuration.validators',
 'piston.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'click>=8.0.1,<9.0.0',
 'coloredlogs>=15.0.1,<16.0.0',
 'more-itertools>=8.7.0,<9.0.0',
 'prompt-toolkit>=3.0.18,<4.0.0',
 'pygments>=2.8.1,<3.0.0',
 'requests-cache>=0.8.1,<0.9.0',
 'requests>=2.25.1,<3.0.0',
 'rich>=10.1.0,<11.0.0']

entry_points = \
{'console_scripts': ['piston = piston:main']}

setup_kwargs = {
    'name': 'piston-cli',
    'version': '1.5.0',
    'description': 'A cli tool with an terminal editor to compile over 35 languages instantly using the piston api.',
    'long_description': '# Piston CLI\n\n[![Linting](https://img.shields.io/github/workflow/status/Shivansh-007/piston-cli/Linting?logo=github)](https://github.com/discord-modmail/modmail/actions/workflows/linting.yml "Lint")\n[![Python](https://img.shields.io/static/v1?label=Python&message=3.9&color=blue&logo=Python&style=flat)](https://www.python.org/downloads/ "Python 3.8 | 3.9")\n[![License](https://img.shields.io/github/license/discord-modmail/modmail?style=flat&label=License)](./LICENSE "License file")\n[![Code Style](https://img.shields.io/static/v1?label=Code%20Style&message=black&color=000000&style=flat)](https://github.com/psf/black "The uncompromising python formatter")\n______________________________________________________________________\n\n**Documentation**: <a href="https://shivansh-007.github.io/piston-cli/" target="_blank">https://shivansh-007.github.io/piston-cli/</a>\n\n**Source Code**: <a href="https://github.com/Shivansh-007/piston-cli" target="_blank">https://github.com/Shivansh-007/piston-cli</a>\n\n______________________________________________________________________\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Shivansh-007',
    'author_email': 'shivansh-007@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Shivansh-007/piston-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
