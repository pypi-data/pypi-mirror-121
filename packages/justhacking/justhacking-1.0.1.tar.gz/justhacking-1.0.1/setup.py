from setuptools import setup, find_packages
import os


VERSION = '1.0.1'
DESCRIPTION = 'Just Hacking is a Python CLI script that stimulates as you are hacking.'

# Setting up
setup(
    name="justhacking",
    version=VERSION,
    author="Divinemonk",
    author_email="<v1b7rc8eb@relay.firefox.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['progressbar', 'tqdm'],
    keywords=['python', 'justhacking', 'divinemonk', 'hacking stimulation', 'cli'],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "justhacking=justhacking.__main__:starthack",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ]
)