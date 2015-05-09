from setuptools import setup
import os

long_desc = ''

if os.path.exists('README.rst'):
    long_desc = open('README.rst').read()

setup(name = 'pygrok',
    version = '0.5.0',
    description = 'A Python library to parse strings and'
        + ' extract information from structured/unstructured data',
    long_description= long_desc,
    url = 'https://github.com/garyelephant/pygrok',
    author = 'garyelephant',
    author_email = 'garygaowork@gmail.com',
    license = 'MIT',
    packages = ['pygrok'],
    include_package_data = True,
    keywords = ['python grok', 'regex'], # arbitrary keywords
    download_url = 'https://github.com/garyelephant/pygrok/tarball/v0.5.0',
    install_requires=['regex']
    )
