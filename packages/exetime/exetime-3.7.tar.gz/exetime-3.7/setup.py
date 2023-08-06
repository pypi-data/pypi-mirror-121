from setuptools import setup, find_packages

VERSION = '3.7'
DESCRIPTION = 'This module is for finding the execution time of a whole program.'

# Setting up
setup(
    name="exetime",
    version=VERSION,
    author="saikat",
    author_email="<sd.saikat369@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'time', 'execution', '', 'process'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)