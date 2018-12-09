# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path
# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

install_requires = ['six', 'SQLAlchemy == 1.3.0b1']
testing_requires = ['pytest', 'pylint', 'flake8', 'pyre-check']

setup(
    name='esframework',
    version='0.0.0',  # Required
    description='A base package to help python developers with ES',
    long_description="A base package to help python developers with "
                     "eventsourcing",
    url='https://github.com/weemen/esframework',  # Optional
    author='Leon Weemen',
    author_email='weemen@leonweemen.nl',
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6',
    ],
    keywords=[
        'eventsourcing',
        'ddd',
        'framework',
        'domain driven design',
        'cqrs'
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=install_requires,
    tests_require=testing_requires,

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    entry_points={  # Optional
        'console_scripts': [
            'esframework.sql.add_store=esframework.cli.sql:create_event_store'
        ],
    },
    data_files=[('config', './config')],
    project_urls={  # Optional
        'Source': 'https://github.com/pypa/sampleproject/',
    },
)
