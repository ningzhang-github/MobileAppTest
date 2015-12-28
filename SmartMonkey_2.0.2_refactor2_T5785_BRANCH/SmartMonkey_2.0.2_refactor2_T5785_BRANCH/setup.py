from distutils.core import setup
import py2exe

DEBUG = True

setup(
    windows=[
        {
            "script": 'SmartMonkey.py'
        }
    ]
)
