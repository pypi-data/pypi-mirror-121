from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='tdl_pybasic',
    packages=['tdl_pybasic'],

    version='0.1.10', # バージョン

    license='MIT', # ライセンス

    install_requires=[],

    author='Atsushi Shibata',
    author_email='shibata@m-info.co.jp',

    url='',

    description='A library for Toushin Digital University Python BASIC.',
    long_description='',
    long_description_content_type='text/markdown',
    keywords='',

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
)