from setuptools import setup, find_packages
import os


VERSION = '1.0.0'
DESCRIPTION = 'Just Hacking is a Python CLI script that stimulates as you are hacking.'

# Setting up
setup(
    name="justhacking",
    version=VERSION,
    author="Divinemonk",
    author_email="<divinemonk@divinemonk.hack>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['progressbar', 'tqdm'],
    keywords=['python', 'justhacking', 'divinemonk', 'hacking stimulation', 'cli'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)