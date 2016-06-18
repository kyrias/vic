# coding=utf-8

from os import path

from setuptools import setup, find_packages


# Get the long description from the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='vic',
    version='0.0.1',

    description='Implementation of the pen-and-paper VIC cipher',
    long_description=long_description,

    url='https://github.com/kyrias/vic',

    author='Johannes Löthberg',
    author_email='johannes@kyriasis.com',

    license='ISC',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: End Users/Desktop',
        'Topic :: Security :: Cryptography',

        'License :: OSI Approved :: ISC License (ISCL)',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='vic cipher cryptography soviet reino häyhänen',

    packages=find_packages(),

    entry_points={
        'console_scripts': [
            'vic=vic.main:main',
        ]
    },
)
