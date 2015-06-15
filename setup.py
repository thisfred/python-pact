"""
pact: A Python implementation of the pact specification.

Copyright (c) 2015
Eric Casteleijn, <thisfred@gmail.com>
"""
from setuptools import setup

import os
import re


def find_version(*file_paths):
    """Get version from python file."""
    with open(os.path.join(os.path.dirname(__file__),
                           *file_paths)) as version_file:
        contents = version_file.read()
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", contents, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='pact',
    version=find_version('pact/__init__.py'),
    author='Eric Casteleijn',
    author_email='thisfred@gmail.com',
    description='Python implementation of the pact specification',
    license='BSD',
    keywords='pact contracts testing REST',
    url='http://github.com/thisfred/python-pact',
    packages=['pact'],
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4'])
