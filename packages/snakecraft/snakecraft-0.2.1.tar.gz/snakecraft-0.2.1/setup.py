# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snakecraft']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['snakecraft = snakecraft.__main__:main']}

setup_kwargs = {
    'name': 'snakecraft',
    'version': '0.2.1',
    'description': 'Describe your Terraform project using Python with inheritance',
    'long_description': '# Snakecraft: Generate Terraform code from Python\n\nHave you ever felt writing Terraform code was very verbose? Have you ever disliked passing variables into layers of modules?\n\nSnakecraft allows you to write your Terraform configuration in Python and generate the necessary Terraform code (as a `.tf.json` file).\n\nPython 3.6 is required at least.\n\n## Installing and running Snakecraft\n\nYou can install Snakecraft using `pip`:\n\n```bash\npip install -U snakecraft\n```\n\nAfterwards, you can author Snakecraft modules/packages in Python code. If you want to\ndive into Snakecraft by reading the [examples](https://github.com/xoraxax/snakecraft/tree/main/examples), you can clone them from Github\nand process them using Snakecraft:\n\n```bash\ngit clone https://github.com/xoraxax/snakecraft.git\n\ncd snakecraft/examples\n\n# The next commands reads snakecraft.ini:\nsnakecraft\n\n# Now we can run Terraform:\ncd simple_example\nterraform init\nterraform plan\n```\n\nAs Snakecraft is still in an early stage, documentation is to be done.\n',
    'author': 'Alexander Schremmer',
    'author_email': 'alex@alexanderweb.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xoraxax/snakecraft',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
