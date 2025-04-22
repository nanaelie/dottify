from setuptools import setup, find_packages

setup(
    name="dottify",
    version="1.0.1",
    author="nae-dev",
    author_email="elienana92@gmail.com",
    description="Une bibliothèque Python pour accéder aux dictionnaires avec la notation par points.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nanaelie/dottify",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
