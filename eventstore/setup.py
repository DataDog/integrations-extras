# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

from codecs import open
from os import path

from setuptools import setup

HERE = path.abspath(path.dirname(__file__))

# Get version info
ABOUT = {}
with open(path.join(HERE, "datadog_checks", "eventstore", "__about__.py")) as f:
    exec(f.read(), ABOUT)

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


def get_dependencies():
    dep_file = path.join(HERE, 'requirements.in')
    if not path.isfile(dep_file):
        return []

    with open(dep_file, encoding='utf-8') as f:
        return f.readlines()


CHECKS_BASE_REQ = 'datadog-checks-base>=5.1.0'

setup(
    name='datadog-eventstore',
    version=ABOUT["__version__"],
    description='Collects Eventstore Metrics',
    long_description=long_description,
    keywords='datadog agent check',
    url='https://github.com/DataDog/integrations-core',
    author='Jason Field',
    author_email='jason.field@calastone.com',
    license='BSD',
    # See https://pypi.org/classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Monitoring',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.7',
    ],
    packages=['datadog_checks.eventstore'],
    # Run-time dependencies
    install_requires=[CHECKS_BASE_REQ],
    extras_require={'deps': get_dependencies()},
    include_package_data=True,
)
