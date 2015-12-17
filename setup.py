"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages, Extension
# To use a consistent encoding
from codecs import open
import os
from os import path
import sys

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

ARCH='64'
SQLPARSER_DIR = './general_sql_parser/'

if sys.maxsize > 2**32:
    ARCH = '64'
else:
    ARCH = '32'

def download_library():
    import urllib

    file_name = "gsp_c_lib.tar.gz"

    url = "http://www.sqlparser.com/dl/gsqlparser_c_linux32_trial_0_3_8.tar.gz"
    if os.name == "nt":
        if ARCH == '32':
            url = "http://www.sqlparser.com/dl/gsqlparser_c_win32_trial_0_3_8.zip"
        else:
            url = "http://www.sqlparser.com/dl/gsqlparser_c_win64_trial_0_3_8.zip"
        file_name = "gsp_c_lib.zip"
    else:
        if ARCH == '64':
            url = "http://www.sqlparser.com/dl/gsqlparser_c_linux64_trial_0_3_8.tar.gz"

    print "Downloading library from '%s'..." % url

    urllib.urlretrieve(url, file_name)

    print "Done!"
    print "Extracting archive..."

    if os.name == "nt":
        import zipfile

        archive = zipfile.ZipFile(file_name, 'r')
        archive.extractall(SQLPARSER_DIR)
    else:
        import tarfile

        archive = tarfile.open(file_name)
        archive.extractall(SQLPARSER_DIR)

    print "Done!"


if not os.path.isdir(SQLPARSER_DIR):
    download_library()

# check again (the user might have downloaded the library)
if os.path.isdir(SQLPARSER_DIR):
    parsebridge = Extension('sqlparser', 
        sources = ['Parser.c', 'Statement.c', 'Node.c', 'ENodeType.c', 'parsebridgemodule.c', 
                                    SQLPARSER_DIR + 'ext/node_visitor/node_visitor.c',
                                    SQLPARSER_DIR + 'ext/expr_traverse/expr_traverse.c',
                                    SQLPARSER_DIR + 'ext/modifysql/modifysql.c' ],
        include_dirs = [ SQLPARSER_DIR + 'core/', 
                            SQLPARSER_DIR + 'ext/collection/includes/',
                            SQLPARSER_DIR + 'ext/expr_traverse/',
                            SQLPARSER_DIR + 'ext/modifysql/',
                            SQLPARSER_DIR + 'ext/node_visitor/' ],
        library_dirs = [ SQLPARSER_DIR + '/lib/' ],
        libraries = [ 'gspcollection', 'gspcore' ],
        define_macros = [ ('_CRT_SECURE_NO_WARNINGS', None), ('DONT_FIX_FRAGMENTS', None), ],
        extra_compile_args = ['-Wno-strict-prototypes'],

    )

    if sys.platform == 'win32' or sys.platform == 'win64':
        parsebridge.extra_link_args = [ '/MANIFEST', '/DEBUG' ]
        parsebridge.extra_compile_args = [ '/Zi' ]

setup (name = 'sqlparser',
    version = '1.0',
    description = 'A package for parsing SQL queries',
    author = 'Timo Djurken',
    url = 'https://github.com/TwoLaid/python-sqlparser',
    license = 'GPL',
    ext_modules = [ parsebridge ])

