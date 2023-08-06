# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['denoc']

package_data = \
{'': ['*']}

install_requires = \
['colores>=0.1.2,<0.2.0']

entry_points = \
{'console_scripts': ['denoc = denoc:main']}

setup_kwargs = {
    'name': 'denoc',
    'version': '1.0.0',
    'description': 'Utilities for compile JavaScript with Deno',
    'long_description': '# Denoc\n\n![CodeQL](https://github.com/UltiRequiem/denoc/workflows/CodeQL/badge.svg)\n![Pylint](https://github.com/UltiRequiem/denoc/workflows/Pylint/badge.svg)\n[![Code Style](https://img.shields.io/badge/Code%20Style-Black-000000.svg)](https://github.com/psf/black)\n[![PyPi Version](https://img.shields.io/pypi/v/denoc)](https://pypi.org/project/denoc)\n![Repo Size](https://img.shields.io/github/repo-size/ultirequiem/denoc?style=flat-square&label=Repo)\n[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)\n![Lines of Code](https://img.shields.io/tokei/lines/github.com/UltiRequiem/denoc?color=blue&label=Total%20Lines)\n\nCompile Deno executables and compress them for all platforms easily.\n\n## Install\n\nYou can install [denoc](https://pypi.org/project/denoc) from PyPI like any other package:\n\n```bash\npip install denoc\n```\n\nTo get the last version:\n\n```bash\npip install git+https:/github.com/UltiRequiem/denoc\n```\n\nIf you use Linux, you may need to install this with sudo to be able to access the command throughout your system.\n\n## Usage\n\nBasic usage:\n\n```bash\ndenoc compileMe.ts\n```\n\nThis will make a directory (`deno_builds`) with executables for all the supported platforms.\n\nOptional flags:\n\n```bash\ndenoc --outputDir deno_dir_output --compress True file.ts\n```\n\n- `outputDir`: The directory where the binaries will be, by default the directory is *deno_build*.\n\n- `compress`: Compress the binaries directory\n\n### License\n\n[This project](https://pypi.org/project/denoc) is licensed under the [MIT License](./LICENSE.md).\n',
    'author': 'Eliaz Bobadilla',
    'author_email': 'eliaz.bobadilladev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/UltiRequiem/denoc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
