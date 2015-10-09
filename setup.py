# -*- coding: utf-8 -*-
from setuptools import setup

try:
    long_description = open('README.rst', 'rt').read()
except Exception:
    long_description = ""

setup(
    name="cfblog",
    description="Awesome CMS for Django",
    long_description=long_description,

    version="0.1.4",
    author='Vinay Karanam',
    author_email="vinayinvicible@gmail.com",

    url='https://github.com/Coverfox/cfblog/',
    license='BSD',

    install_requires=[
        "beautifulsoup4",
        "Django>=1.8,<1.9",
        "django-jsonfield==0.9.15",
        "django-tagging==0.4",
        "mistune==0.7.1",
        "Pillow==2.9.0"
    ],
    packages=['cfblog', 'cfblog.migrations'],

    zip_safe=True,
)
