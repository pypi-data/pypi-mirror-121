# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blint']

package_data = \
{'': ['*'], 'blint': ['data/*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'lief>=0.11.5,<0.12.0', 'rich>=10.10.0,<11.0.0']

entry_points = \
{'console_scripts': ['blint = blint.cli:main']}

setup_kwargs = {
    'name': 'blint',
    'version': '0.0.0',
    'description': 'Linter for binary files powered by lief',
    'long_description': '# Introduction\n\n**COMING SOON**\n\nblint is a simple Binary Linter to check the security properties and hardcoded credentials in your executables. It is powered by [lief](https://github.com/lief-project/LIEF)\n\nSupported formats:\n\n- ELF\n- PE\n- Mach-O\n\n## Installation\n\n- Install python 3.8 or 3.9\n\n```bash\npip3 install blint\n```\n\n## References\n\n- [lief examples](https://github.com/lief-project/LIEF/tree/master/examples/python)\n- [checksec](https://github.com/Wenzel/checksec.py)\n',
    'author': 'Prabhu Subramanian',
    'author_email': 'prabhu@appthreat.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://rosa.cx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
