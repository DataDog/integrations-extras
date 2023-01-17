import re
from ast import literal_eval
from codecs import open
from os import path

from setuptools import setup

HERE = path.dirname(path.abspath(__file__))

# Get version info
ABOUT = {}
with open(path.join(HERE, 'datadog_checks', 'kamailio', '__about__.py')) as f:
    # noinspection BuiltinExec
    exec(f.read(), ABOUT)

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


def parse_pyproject_array(name):
    pattern = r'^{} = (\[.*?\])$'.format(name)
    with open(path.join(HERE, 'pyproject.toml'), 'r', encoding='utf-8') as f:
        # Windows \r\n prevents match
        contents = '\n'.join(line.rstrip() for line in f.readlines())
    array = re.search(pattern, contents, flags=re.MULTILINE | re.DOTALL).group(1)
    return literal_eval(array)


dependencies = parse_pyproject_array('dependencies')
optional_deps = parse_pyproject_array('deps')
classifiers = parse_pyproject_array('classifiers')
CHECKS_BASE_REQ = dependencies[0]

setup(
    name='datadog-kamailio',
    version=ABOUT['__version__'],
    description='The kamailio check',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='datadog agent kamailio check',
    # The project's main homepage.
    url='https://github.com/DataDog/integrations-extras',
    # Author details
    author='Tyler Moore',
    author_email='tmoore@dopensource.com',
    # License
    license='BSD-3-Clause',
    # See https://pypi.org/classifiers
    classifiers=classifiers,
    # The package we're going to ship
    packages=['datadog_checks.kamailio'],
    # Run-time dependencies
    install_requires=dependencies,
    extras_require={'deps': optional_deps},
    # Extra files to ship with the wheel package
    include_package_data=True,
)
