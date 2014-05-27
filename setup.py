#!/usr/bin/env python
# coding: utf-8

# Copyright 2014 Foxdog Studios Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from setuptools import setup

setup(
    name='pyddp',
    version='0.2.0',
    description='Distributed Data Protocol (DDP)',
    author='Peter Sutton',
    author_email='foxxy@foxdogstudios.com',
    url='https://github.com/foxdog-studios/pyddp',
    license='Apache License v2.0',
    packages=[
        'ddp',
        'ddp.connection',
        'ddp.message',
        'ddp.message.client',
        'ddp.message.server',
        'ddp.pod',
        'ddp.pubsub',
    ],
    package_data={
        '': ['LICENSE.txt']
    },
    install_requires=['ws4py'],
    test_suite='tests',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

