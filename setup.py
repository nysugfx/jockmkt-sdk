from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.rst').read_text(encoding="utf-8")

setup(
    name="jockmkt-sdk",
    version="0.1",
    description="a basic package allowing the user to interact with jockmkt's API",
    long_description=long_description,
    url='https://github.com/nysugfx/jockmkt-sdk',
    author='Alexander Friedman/nysugfx',
    author_email='nysu.gfx@gmail.com',
    license='MIT',
    classifiers=[
        "development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10"
    ],
    keywords="jock mkt, api, apitools, jockmkt",
    packages=find_packages(where='jockmkt-sdk'),
    python_requires=">=3.10, <4",
    install_requires=['requests', 'DateTime'],
    project_urls={
        "Bug Reports": "https://github.com/nysugfx/jockmkt-sdk/issues",
    }
)
