#!/usr/bin/python3
import os

from setuptools import setup

here = os.path.dirname(os.path.abspath(__file__))

install_requires = [
    "click",
]

extras_require = {
    ':sys_platform != "win32" and sys_platform != "cygwin" and platform_python_implementation != "pypy"': [
        "uvloop",
    ],
    "dns": [
        "dnspython",
    ],
    "whois": [
        "requests",
        "mecache",
    ],
    "proxy": [
        "pysocks",
    ],
}

entry_points = {
    "console_scripts": [
        f"py-{name[:-3].replace('_', '-')} = usefuls.{name[:-3]}:main"
        for name in os.listdir(os.path.join(here, "usefuls"))
        if (
            os.path.isfile(os.path.join(here, "usefuls", name))
            and name.endswith(".py")
            and name != "__init__.py"
        )
    ]
}

setup_kwargs = {
    "name": "usefuls",
    "version": "0.0.0",
    "description": "Some useful scripts",
    "long_description": "",
    "author": "abersheeran",
    "author_email": "me@abersheeran.com",
    "maintainer": None,
    "maintainer_email": None,
    "url": "https://github.com/abersheeran/usefuls",
    "packages": ["usefuls"],
    "package_data": {"": ["*"]},
    "install_requires": install_requires,
    "extras_require": extras_require,
    "entry_points": entry_points,
    "python_requires": ">=3.6.1,<4.0.0",
}


setup(**setup_kwargs)
