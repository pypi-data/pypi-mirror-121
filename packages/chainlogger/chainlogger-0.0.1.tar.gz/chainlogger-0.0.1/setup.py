from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.1'
DESCRIPTION = 'Log data into blockchain'
LONG_DESCRIPTION = 'A package that register a project, vendor and a log into a selected blockchain.'

setup(
    name="chainlogger",
    version=VERSION,
    author="MERT YILMAZ",
    author_email="<mert@omlira.com>",
    description=DESCRIPTION,
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['web3'],
    keywords=['python', 'blockchain', 'logging'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3"
    ]
)
