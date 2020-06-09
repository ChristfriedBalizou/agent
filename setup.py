import os
import re
import codecs

from setuptools import setup, find_package


CURRENT_DIRECTORY = os.path.realpath(os.path.dirname(__file__))

SETUP_REQUIRES = (
    "pytest-runner"
)

INSTALL_REQUIRES = ()

TESTS_REQUIRES = (
    "pytest",
    "pytest-pep8",
    "pytest-flakes",
)

EXTRAS_REQUIRE = {
    "dev": TESTS_REQUIRES
}

ENTRY_POINTS = {
    "console_scripts": {
        "agent": "agent.main:main"
    }
}


def read(*paths):
    """This function aim to read from special
    files with special formatting using python
    codecs library.
    """

    path = os.path.join(CURRENT_DIRECTORY, *paths)

    with codecs.open(path) as stream:
        return stream.read()


def find_version(*file_paths):
    """Retrieve the version from a given file
    """
    version_file = read(*file_paths)
    version_match = re.search(
        r"^__version__ = [\"']([^\"'']*)[\"']",
        version_file,
        re.M
    )

    if version_match:
        return version_match.group(1)

    raise RuntimeError("Unable to find version")


setup(
    name="agent",
    version=find_version("agent", "__init__.py"),
    description="Linux application luncher service and cron controller",
    long_description=read("README.rst"),
    entry_points=ENTRY_POINTS,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Environment :: Console",
        "License :: OSI Approved :: GPL License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="agent docker kubernetes orchestrate",
    author="Christfried BALIZOU",
    author_email="christfriedbalizou@gmail.com",
    license="GPL",
    packages=find_package(),
    setup_requires=SETUP_REQUIRES,
    install_requires=INSTALL_REQUIRES,
    tests_requires=TESTS_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    include_package_date=True,
)
