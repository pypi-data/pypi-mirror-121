# -*- coding: utf-8 -*-

# auxilium
# --------
# Python project for an automated test and deploy toolkit.
#
# Author:   sonntagsgesicht
# Version:  0.1.7, copyright Thursday, 30 September 2021
# Website:  https://github.com/sonntagsgesicht/auxilium
# License:  Apache License 2.0 (see LICENSE file)


from logging import log, INFO
from os import getcwd
from os.path import basename

from .const import TEST_PATH, ICONS
from .system_tools import module, del_tree, join


def coverage(pkg=basename(getcwd()), test_dir=TEST_PATH, venv=None):
    """check code coverage of tests"""
    log(INFO, ICONS["coverage"] + 'run test coverage scripts')
    return coverage_coverage(pkg, test_dir, venv)


def coverage_test(test_dir=TEST_PATH, venv=None):
    """check code coverage of tests with native test"""
    return module('test', '--coverage -D `pwd`/coverage_data %s' % test_dir,
                  level=INFO, venv=venv)


def coverage_pytest(test_dir=TEST_PATH, venv=None):
    """check code coverage of tests with pytest"""
    # --cov=[SOURCE]
    # --cov-fail-under = MIN
    return module('pytest', '--cov %s --cov-fail-under=80 ' % test_dir,
                  level=INFO, venv=venv)


def coverage_coverage(
        pkg=basename(getcwd()), test_dir=TEST_PATH, venv=None):
    """check code coverage of tests with coverage"""
    cmd = 'run --include="%s*"' \
          ' --module unittest discover %s -v -p "*.py"' % (pkg, test_dir)
    res = module('coverage', cmd, venv=venv)
    module('coverage', 'report -m', level=INFO, venv=venv)
    return res


def cleanup(test_dir=TEST_PATH):
    """remove temporary files"""
    log(INFO, ICONS["clean"] + 'clean coverage')
    # removed coverage data files incl. files in test dir
    files = ".coverage", "coverage.xml", "htmlcov"
    del_tree(*files)
    del_tree(*(join(test_dir, f) for f in files))
    return 0
