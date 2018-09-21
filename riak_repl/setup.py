from codecs import open  # To use a consistent encoding
from os import path

from setuptools import setup

HERE = path.dirname(path.abspath(__file__))

# Get version info
ABOUT = {}
with open(path.join(HERE, 'datadog_checks', 'riak_repl', '__about__.py')) as f:
    exec(f.read(), ABOUT)

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


CHECKS_BASE_REQ = 'datadog-checks-base'


setup(
    name='datadog-riak_repl',
    version=ABOUT['__version__'],
    description='The Riak_repl check',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='datadog agent riak_repl check',

    # The project's main homepage.
    url='https://github.com/DataDog/integrations-extras',

    # Author details
    author='Britt Treece',
    author_email='britt.treece@gmail.com',

    # License
    license='BSD-3-Clause',

    # See https://pypi.org/classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Monitoring',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    # The package we're going to ship
    packages=['datadog_checks', 'datadog_checks.riak_repl'],

    # Run-time dependencies
    install_requires=[CHECKS_BASE_REQ],

    # Extra files to ship with the wheel package
    include_package_data=True,
)
