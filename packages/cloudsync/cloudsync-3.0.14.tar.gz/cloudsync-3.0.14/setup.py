#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['cloudsync',
 'cloudsync.command',
 'cloudsync.oauth',
 'cloudsync.providers',
 'cloudsync.sync',
 'cloudsync.tests',
 'cloudsync.tests.fixtures']

package_data = \
{'': ['*']}

install_requires = \
['arrow~=0.17.0',
 'pystrict',
 'msgpack',
 'requests_oauthlib',
 'python-daemon',
 'xxhash',
 'urllib3>=1.25.3',
 'watchdog']

extras_require = \
{":python_version < '3.7'": ['dataclasses'],
 ":sys_platform == 'win32'": ['pywin32'],
 'all': ['cloudsync-gdrive~=2.0.0',
         'cloudsync-onedrive~=3.1.9',
         'boxsdk[jwt]',
         'dropbox>=10.3.0',
         'six>=1.14.0',
         'boxsdk>=2.9.0'],
 'box': ['boxsdk>=2.9.0'],
 'boxcom': ['boxsdk[jwt]'],
 'dropbox': ['dropbox>=10.3.0', 'six>=1.14.0'],
 'gdrive': ['cloudsync-gdrive~=2.0.0'],
 'onedrive': ['cloudsync-onedrive~=3.1.9']}

entry_points = \
{'console_scripts': ['cloudsync = cloudsync.command:main']}

setup(name='cloudsync',
      version='3.0.14',
      description='cloudsync enables simple cloud file-level sync with a variety of cloud providers',
      author='Atakama, LLC',
      author_email='dev-support@atakama.com',
      url='https://github.com/atakamallc/cloudsync',
      packages=packages,
      package_data=package_data,
      install_requires=install_requires,
      extras_require=extras_require,
      entry_points=entry_points,
      python_requires='>=3.6',
     )
