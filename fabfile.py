#!/usr/bin/env python3
# coding=utf-8
from __future__ import (
    absolute_import, division, print_function, unicode_literals,
)

from fabric.api import local


def clean():
    local(
        'rm -rf '
        'build '
        'dist '
        '*.egg '
        'cfblog/__pycache__ '
        'cfblog/*.pyc '
        'exmaple/__pycache__ '
        'example/*.pyc'
    )


def docs():
    local("./bin/docs")
    local("./bin/python setup.py upload_sphinx --upload-dir=docs/html")


def release():
    clean()
    local("python setup.py clean")
    local("python setup.py sdist bdist_wheel")
    local("twine upload dist/*")
