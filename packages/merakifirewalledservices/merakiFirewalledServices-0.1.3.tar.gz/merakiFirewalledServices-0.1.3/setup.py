# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['merakifirewalledservices']

package_data = \
{'': ['*']}

install_requires = \
['Pygments==2.10.0',
 'aiohttp==3.7.4.post0',
 'async-timeout==3.0.1',
 'attrs==21.2.0',
 'certifi==2021.5.30',
 'chardet==4.0.0',
 'charset-normalizer==2.0.5',
 'click==8.0.1',
 'colorama==0.4.4',
 'commonmark==0.9.1',
 'idna==3.2',
 'meraki==1.12.0',
 'multidict==5.1.0',
 'requests==2.26.0',
 'rich==10.9.0',
 'typing-extensions==3.10.0.2',
 'urllib3==1.26.6',
 'yarl==1.6.3']

entry_points = \
{'console_scripts': ['merakiFirewalledServices = '
                     'merakifirewalledservices.merakiFirewalledServices:main']}

setup_kwargs = {
    'name': 'merakifirewalledservices',
    'version': '0.1.3',
    'description': 'Get Security Appliance Firewalled Services status from Meraki dashboard',
    'long_description': '# Get Security Appliance Firewalled Services status from Meraki dashboard\n\nThe script collects the status of the Meraki MX firewalled services status from the Meraki Dashboard and prints a report.\n\n## Installation\n\npython -m pip install merakifirewalledservices\n\n\n## Usage\n\nProvide API Key and Organization ID from CLI:\n\n```\nmerakiFirewalledServices --apikey <myApiKey> --orgid <myOrgId>\n```\n\nOr from env vars:\n\n```\nexport APIKEY=<myApiKey>\nexport ORGID=<myOrgId>\n```\n\nIf OrgId is not provided the script prints the list of accessible organization with the provides API Key.\n',
    'author': 'Gian Paolo Boarina',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/routetonull/merakiFirewalledServices',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
