import pathlib
from setuptools import setup

here = pathlib.Path(__file__).parent
readme = (here / "README.md").read_text()

setup(
    name = "Malas",
    version = "1.0.210929.0001",
    description = "Malas (Multi-vendor automation leverage at slouching)",
    long_description = readme,
    long_description_content_type = "text/markdown",
    url = "https://github.com/destrianto/malas",
    download_url = "https://github.com/destrianto/malas/releases/download/1.0.210929.0001/malas_1.0.210929.0001.zip",
    author = "Ade Destrianto",
    author_email = "ade.destrianto@mail.ru",
    license = "MIT",
    classifiers = [
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.9",
        "Topic :: System :: Networking"
    ],
    keywords = [
        "multi-vendor",
        "network",
        "automation"
    ],
    packages = [
        "malas"
    ],
    install_requires = [
        "netmiko>=3.4.0",
        "pythonping>=1.1.0"
    ],
    python_requires = ">=3.9"
)