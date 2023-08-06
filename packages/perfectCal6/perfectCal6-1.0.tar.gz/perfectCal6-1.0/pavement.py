from paver.easy import *
import paver.doctools
from paver.setuputils import setup
from setuptools import find_packages

setup(
    name="perfectCal6",
    packages= find_packages(),
    version="1.0",
    author="narahari_nguyen",
    author_email="nguyenelizabeth48@gmail.com",
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite = 'tests',
)

options(
    minilib = Bunch(
        extra_files=["doctools"],
        versioned_name=False
    )
)

@task #use command: paver run
def run():
    sdist()
    checkSetuptools()
    test()
    pass

@task
@needs('generate_setup', 'minilib', 'setuptools.command.sdist')
def sdist():
    """Overrides sdist to make sure that our setup.py is generated."""
    pass

@task
def checkSetuptools():
    try:
        import setuptools
    except ImportError:
        sh("pip install setuptools")
    pass

@task
def checkPaver():
    try:
        import paver
    except ImportError:
        sh("pip install paver")
    pass

@task
def test():
    try:
        import pytest
    except ImportError:
        sh("pip install pytest")

    sh("pytest")
    pass

