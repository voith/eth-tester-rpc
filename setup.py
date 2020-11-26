#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import (
    find_packages,
    setup,
)

extras_require = {
    'test': [
        "pytest>=4.4.0",
        "pytest-xdist",
        "tox>=2.9.1,<3",
        "requests>=2.16.0,<3.0.0",
        "eth-account>=0.5.3,<0.6.0",
        "eth-abi>=2.0.0b4,<3.0.0",
        "web3>=5.0.0b2,<6.0.0",
        "splinter>=0.10.0,<1.0.0",
    ],
    'lint': [
        "flake8==3.4.1",
        "isort>=4.2.15,<5",
    ],
    'doc': [
        "Sphinx>=1.6.5,<2",
        "sphinx_rtd_theme>=0.1.9",
    ],
    'dev': [
        "bumpversion>=0.5.3,<1",
        "pytest-watch>=4.1.0,<5",
        "wheel",
        "twine",
        "ipython",
    ],
    'gevent': [
        "gevent>=1.1.1,<1.2.0",
    ]
}

extras_require['dev'] = (
    extras_require['dev'] +
    extras_require['test'] +
    extras_require['lint'] +
    extras_require['doc']
)

setup(
    name='eth-tester-rpc',
    # *IMPORTANT*: Don't manually change the version here. Use `make bump`, as described in readme
    version='0.5.0-beta.1',
    description="""Python TestRPC for ethereum""",
    long_description_markdown_filename='README.md',
    author='voith',
    author_email='voithjm1@gmail.com',
    url='https://github.com/voith/eth-tester-rpc',
    include_package_data=True,
    install_requires=[
        "eth-utils>=1,<2",
        "toolz>=0.9.0,<1.0.0;implementation_name=='pypy'",
        "cytoolz>=0.9.0,<1.0.0;implementation_name=='cpython'",
        "eth-tester[py-evm]==0.5.0b3",
        "eth-hash[pysha3]>=0.1.4,<1.0.0;implementation_name=='cpython'",
        "eth-hash[pycryptodome]>=0.1.4,<1.0.0;implementation_name=='pypy'",
        'json-rpc>=1.10.3',
        'Werkzeug>=0.11.10',
        'click>=6.6',
    ],
    setup_requires=['setuptools-markdown'],
    python_requires='>=3.6, <4',
    extras_require=extras_require,
    py_modules=['eth_tester_rpc'],
    license="MIT",
    zip_safe=False,
    keywords='ethereum',
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    entry_points={
        'console_scripts': ['py-testrpc=eth_tester_rpc.cli:runserver'],
    },
)
