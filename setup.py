#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from cache_tools import __version__


INSTALL_REQUIRES = [
]

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Communications',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Programming Language :: Python :: 2.7',
]

setup(
    name='sisu-cache-tools',
    version=__version__,
    description='Management tools for managing the cache',
    author='Martin Koistinen',
    author_email='mkoistinen@gmail.com',
    url='https://github.com/mkoistinen/sisu-cache-tools',
    packages=['cache_tools', ],
    install_requires=INSTALL_REQUIRES,
    license='LICENSE.txt',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    long_description=open('README.md').read(),
    include_package_data=True,
    zip_safe=False,
    download_url='https://github.com/mkoistinen/sisu-cache-tools/tarball/0.0.1',
)