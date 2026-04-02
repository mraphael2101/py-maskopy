"""
This file tells Python that the 'maskopy' folder is a formal library.
By having this file, the IDE will provide:
- Autocomplete: Suggesting method names while you type.
- Tooltips: Showing documentation for each masking method.
- Real-time Error Checking: Highlighting typos or missing parameters.

It also allows the project to be installed in "editable mode," meaning any
changes you make to the masking logic are picked up immediately by your
scripts and CI/CD pipelines without needing to reinstall.
"""

from setuptools import setup

setup(
    name="maskopy-local",
    version="0.1.0",
    packages=["maskopy"],
    description="Local implementation of core masking algorithms inspired by the official Maskopy framework.",
    python_requires=">=3.8",
)
