#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#  Copyleft 2015-2021  PacMiam
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
# ------------------------------------------------------------------------------

from setuptools import find_packages, setup

setup(
    name='Geode-GEM',
    version='0.12.0',
    author='PacMiam',
    author_email='pacmiam@tuxfamily.org',
    description='Geode-GEM is an interface to manage emulators and games',
    long_description='GEM (Graphical Emulators Manager) is a GTK+ Graphical '
                     'User Interface (GUI) for GNU/Linux which allows you to '
                     'easily manage your emulators. This software aims to '
                     'stay the simplest.',
    keywords='gtk+ emulators games',
    url='https://gem.tuxfamily.org',
    project_urls={
        'Archives': 'https://download.tuxfamily.org/gem/releases',
        'Source': 'https://framagit.org/geode/gem',
        'Tracker': 'https://framagit.org/geode/gem/issues',
    },
    packages=find_packages(exclude=['tools', 'test']),
    include_package_data=True,
    python_requires='~= 3.8',
    install_requires=[
        'PyGobject ~= 3.32',
        'pyxdg ~= 0.26',
    ],
    extras_require={
        'dev': [
            'flake8',
            'pytest',
            'tox',
        ],
    },
    entry_points={
        'console_scripts': [
            'gem-ui = geode_gem.__main__:main',
            'geode-gem = geode_gem.__main__:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: X11 Applications :: GTK',
        'Intended Audience :: End Users/Desktop',
        ('License :: OSI Approved :: '
         'GNU General Public License v3 or later (GPLv3+)'),
        'Natural Language :: French',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Games/Entertainment',
        'Topic :: Utilities',
    ],
)
