from setuptools import setup, find_packages
from dottify.__version__ import __version__

setup(
    name="dottify",
    version=__version__,
    author="nae-dev",
    author_email="nae.devp@gmail.com",
    description="A Python library to access dictionaries using dot notation.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nanaelie/dottify",
    project_urls={
        "Source": "https://github.com/nanaelie/dottify",
        "Bug Tracker": "https://github.com/nanaelie/dottify/issues",
        "Documentation": "https://github.com/nanaelie/dottify#readme",
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires='>=3.6',
    license="MIT",
)
