import os
import re
import setuptools
import subprocess
import sys

here = os.path.abspath(os.path.dirname(__file__))

repository_name = "Neradoc/discotool"
current_tag = subprocess.run("git describe --tags --abbrev=0",
	capture_output = True,
	encoding = "utf-8",
	shell = True,
).stdout.strip()

long_description = "Moved to [discotool](https://pypi.org/project/discotool/)."

required_modules = [
    "discotool",
]

setuptools.setup(
    name="discotool-for-microcontrollers",
    author="Neradoc",
    author_email="neraOnGit@ri1.fr",
    description="Discover, list, and use USB microcontoller boards.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Neradoc/discotool",
    license="MIT",
    project_urls={
        "Bug Tracker": "https://github.com/Neradoc/discotool/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    packages=[],
    python_requires=">=3.6",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    install_requires=required_modules,
    entry_points={},
    keywords="",
)
