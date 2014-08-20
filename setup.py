from distutils.core import setup
import py2exe

setup(
    windows = [
        {
            "script": "Mytago.py",
            "icon_resources": [(1, "mytago.ico")]
        }
    ],
)

