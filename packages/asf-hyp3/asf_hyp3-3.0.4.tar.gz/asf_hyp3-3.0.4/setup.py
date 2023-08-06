import sys

RETIREMENT_MESSAGE = \
"""
As of September 30, 2021, ASF's beta HyP3 (version 1) service available at 
https://hyp3.asf.alaska.edu/ has been retired in favor of ASF's new On Demand
service powered by HyP3 version 2.

Programmatic usage of HyP3 v2 is available via the HyP3 SDK:
    https://hyp3-docs.asf.alaska.edu/using/sdk/
    
For more information, please check out the full HyP3 documentation at: 
    https://hyp3-docs.asf.alaska.edu/
"""

if 'sdist' not in sys.argv:
    sys.exit(RETIREMENT_MESSAGE)

from codecs import open
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='asf_hyp3',
    version='3.0.4',

    description='Api for ASF\'s hyp3 system',
    long_description=long_description,

    url='https://github.com/asfadmin/hyp3-api',

    author='ASF Student Development Team 2017',
    author_email='eng.accts@asf.alaska.edu',

    license="License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",

    classifiers=['Development Status :: 7 - Inactive'],

    packages=find_packages(),
    package_data={
        'asf_hyp3': ['messages.json']
    },

    install_requires=['requests>=2.14.0', 'pyshp>=1.2.11', 'pygeoif>=0.7']
)
