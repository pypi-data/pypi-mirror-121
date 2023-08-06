from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.3.7'
DESCRIPTION = 'This module is for finding the execution time of a whole program'

# Setting up
setup(
    name="exetime",
    version=VERSION,
    author="saikat",
    author_email="<sd.saikat369@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'execute','process','time','execution','compile'],
    classifiers=[
        "Development Status :: 5 - Production/Stable ",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)