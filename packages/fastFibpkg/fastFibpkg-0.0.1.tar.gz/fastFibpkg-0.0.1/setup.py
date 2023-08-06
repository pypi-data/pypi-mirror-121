from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Function for Fibonacci numbers.'

# Setting up
setup(
    name="fastFibpkg",
    version=VERSION,
    author="LuisF (Luis Fonseca)",
    author_email="<luis.barreiros12345@live.com.pt>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'fibonnaci', 'fast', 'modular arithmethic'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
