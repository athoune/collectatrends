#!/usr/bin/env python
#from distutils.core import setup
from setuptools import setup, find_packages

setup(name="Collecta Trends",
      version="0.1",
      description="Collecta evolution",
      license="GPL-3",
      author="Mathieu Lecarme",
      url="http://github.com/athoune/collectatrends",
      packages=['collectatrends'],
      package_dir={'': 'src/'},
      keywords= "rrd",
      zip_safe = True,
      install_requires=["roundrobin", "pyyaml"],
      scripts=['bin/collectatrends'])