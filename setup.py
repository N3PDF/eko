# -*- coding: utf-8 -*-
# Installation script for python
from setuptools import setup, find_packages

# write version on the fly - inspired by numpy
MAJOR = 0
MINOR = 6
MICRO = 0
ISRELEASED = False
SHORT_VERSION = "%d.%d" % (MAJOR, MINOR)
VERSION = "%d.%d.%d" % (MAJOR, MINOR, MICRO)


def write_version_py(filename="src/eko/version.py"):
    cnt = """
# THIS FILE IS GENERATED FROM SETUP.PY
""\"This module is autogenerated by ``setup.py`` at build time.
This scheme is inspired by :mod:`numpy.version`""\"

major = %(major)d
short_version = '%(short_version)s'
version = '%(version)s'
full_version = '%(full_version)s'
is_released = %(isreleased)s
"""
    FULLVERSION = VERSION
    if not ISRELEASED:
        FULLVERSION += "-develop"

    a = open(filename, "w")
    try:
        a.write(
            cnt
            % {
                "major": MAJOR,
                "short_version": SHORT_VERSION,
                "version": VERSION,
                "full_version": FULLVERSION,
                "isreleased": str(ISRELEASED),
            }
        )
    finally:
        a.close()

def setup_package():
    # write version
    write_version_py()
    # paste Readme
    with open("README.md", "r") as fh:
        long_description = fh.read()
    # do it
    setup(name='eko',
        version=VERSION,
        description='Evolution Kernel Operator',
        long_description=long_description,
        long_description_content_type="text/markdown",
        author = 'A. Candido, S. Carrazza, J. Cruz-Martinez, F. Hekhorn',
        author_email='stefano.carrazza@cern.ch',
        url='https://github.com/N3PDF/eko',
        package_dir={'': 'src'},
        packages=find_packages('src'),
        package_data = {
            '' : ['doc/source/img/Logo.png'],
        },
        classifiers=[
            'Operating System :: Unix',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Topic :: Scientific/Engineering',
            'Topic :: Scientific/Engineering :: Physics',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        ],
        install_requires=[
            'numpy',
            'scipy',
            'numba',
            'pyyaml',
        ],
        setup_requires=[
            'wheel'
        ],
        python_requires='>=3.7'
    )

if __name__ == "__main__":
    setup_package()
