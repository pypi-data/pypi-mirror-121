# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dora_lakehouse_aws']

package_data = \
{'': ['*']}

install_requires = \
['dora-lakehouse>=0.0.11,<0.0.12']

extras_require = \
{'boto3': ['boto3>=1.18.51,<2.0.0'], 'pyspark': ['pyspark>=3.0.1,<4.0.0']}

setup_kwargs = {
    'name': 'dora-lakehouse-aws',
    'version': '0.0.1',
    'description': 'Dora Lakehouse for AWS',
    'long_description': '# Dora Project\n\nWelcome to Dora community :blue_heart:\n\nThe primary purpose of this community is to collaborate on projects focused on data and analytics. We want people to work better together. This is a community we build together, and we need your help to make it the best it can be.\n\n> Before start remember that contributions to this repository should follow its [contributing guidelines](.github/CONTRIBUTING.md) and [code of conduct](.github/CODE_OF_CONDUCT.md).\n\n## Open Source\n\nWhant to learn more about [Open Source](https://opensource.org/) projects?\n\nThe links below may be helpfull:\n\n- <https://opensource.guide/>\n- <https://todogroup.org/guides/>\n- <https://guides.github.com/>\n- <https://choosealicense.com/licenses/>\n- <https://www.contributor-covenant.org/>\n- <https://mozillascience.github.io/working-open-workshop/>\n\n---\n\n[Dora Project](https://github.com/doraproject) is a recent open-source project based on technology developed at [Compasso UOL](https://compassouol.com/)\n',
    'author': 'Didone',
    'author_email': 'didone@live.com',
    'maintainer': 'DataLabs',
    'maintainer_email': 'time.dataanalytics.datalabs@compasso.com.br',
    'url': 'https://github.com/doraproject/lakehouse-aws',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
