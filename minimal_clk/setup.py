from distutils.core import setup, Extension

setup(name="clock",version="1.0",ext_modules=[Extension("clock",["minimal_clk.c"])])