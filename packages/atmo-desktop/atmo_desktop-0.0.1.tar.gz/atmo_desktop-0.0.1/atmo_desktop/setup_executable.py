import cx_Freeze
from cx_Freeze import *

# Run this file with py setup.py build #

setup(
    name = "atmoSniffer",
    options = {'build_exe':{'packages': ['bitstring', 'cffi', 'cycler', 'ecdsa', 'esptool']}}, 
    executables = [
        Executable(
            "atmoSniffer.py",
            )
        ]
    )
