"""A setuptools based setup module.

Based on https://github.com/pypa/sampleproject.

"""
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    with open(path.join(here, 'HISTORY.rst'), encoding='utf-8') as g:
        long_description = f.read() + '\n\n' + g.read()

setup(
    name='django-view-export',
    version='1.0.0',
    description='Export CSV reports of database views.',
    long_description=long_description,
    url='https://gitlab.com/Sturm/django-view-export',
    author='Ben Sturmfels',
    author_email='ben@sturm.com.au',
    license='Apache License, Version 2.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    python_requires='>=3.6',
    install_requires=[
        'Django>=3.2',
    ],
    project_urls={
        'Source': 'https://gitlab.com/Sturm/django-view-export',
        'Bug Reports': 'https://gitlab.com/Sturm/django-view-export/-/issues',
    }
)
