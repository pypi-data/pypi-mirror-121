import os

from setuptools import Command, find_packages, setup

requirements = [
    "numpy",
    "pandas",
    "plotly",
    "jupyter",
    "jupytext",
    "tqdm",
    "matplotlib",
]

dev_requirements = [
    "black",
    "bumpversion",
    "flake8",
    "isort",
    "pytest",
    "coverage",
    "pytest-cov",
    "radon[flake8]",
    "tox",
]


class CleanCommand(Command):
    """
    Custom clean command to tidy up the project root.
    https://github.com/trigger/trigger/blob/develop/setup.py#L26
    """

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        assert os.getcwd() == self.cwd, "Must be in package root: %s" % self.cwd
        os.system("rm -rf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info")


setup(
    name="poepp",
    version="0.1.2",
    author="Kyle Harrison",
    author_email="kyleharrison94@hotmail.com",
    packages=find_packages(),
    license="LICENSE.md",
    description=(
        "A Python package for predicting currency prices in the game Path of Exile"
    ),
    long_description=open("README.md").read(),
    install_requires=requirements,
    extras_require={"dev": dev_requirements},
    cmdclass={
        "clean": CleanCommand,
    },
)
