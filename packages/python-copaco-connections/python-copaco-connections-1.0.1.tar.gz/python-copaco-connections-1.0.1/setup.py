from setuptools import setup

# read the contents of README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'python-copaco-connections',         
  packages=['copaco', 'copaco.models', 'copaco.constants', 'copaco.types', 'copaco.temp'],
  version = '1.0.1',
  license='GPL-3.0-or-later',
  description = 'Easy python integrations for the Copaco Customer Connections',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Alexander Schillemans',
  author_email = 'alexander.schillemans@lhs.global',
  url = 'https://github.com/alexanderlhsglobal/python-copaco-connections',
  download_url = 'https://github.com/alexanderlhsglobal/python-copaco-connections/archive/refs/tags/1.0.1.tar.gz',
  keywords = ['copaco', 'api', 'customer connections'],
  install_requires=[
          'requests',
          'pandas',
          'xmltodict'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Programming Language :: Python :: 3.6',
  ],
)