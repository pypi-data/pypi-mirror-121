from setuptools import setup, find_packages
import os

VERSION = '0.0.1'
DESCRIPTION = 'Reading Atmosniffer device data.'
LONG_DESCRIPTION = 'A package that allows to listen to atmosniffer devices and plot data into graphs.'

# Setting up
setup(
    name="atmo_desktop",
    version=VERSION,
    author="Miguel Castrejon",
    author_email="<miguelcastrejon@mail.weber.edu.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['PyQt5', 'serial', 'webbrowser', 'pandas', 'csv', 'os', 'cx_Freeze', 'matplotlib', 'io', 'datetime'],
    keywords=['python', 'atmoSniffer'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ]
)