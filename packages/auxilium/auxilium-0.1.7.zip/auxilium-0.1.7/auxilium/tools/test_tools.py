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
from .system_tools import python as _python, module, del_tree


def test(test_dir=TEST_PATH, venv=None):
    """test code by running tests"""
    log(INFO, ICONS["test"] + 'run test scripts')
    return test_unittest(test_dir, venv)


def test_unittest(test_dir=TEST_PATH, venv=None):
    """test code by running unittest"""
    return module(
        'unittest', 'discover %s -v -p "*.py"' % test_dir,
        level=INFO, venv=venv)


def test_pytest(test_dir=TEST_PATH, venv=None):
    """test code by running pytest"""
    return module('pytest', test_dir + ' unittests.py',
                  level=INFO, venv=venv)


def doctests(pkg=basename(getcwd()), venv=None):
    """test code in doc string (doctest)"""
    log(INFO, ICONS["doctest2"] + 'run doctest scripts')
#     cmd = '''
# import doctest, %s as pkg;
# def _doctest_recursively(pkg, *args, **kwargs):
#     import doctest
#     import inspect
#     pkg = __import__(pkg) if isinstance(pkg, str) else pkg
#     if inspect.ismodule(pkg):
#         print(pkg.__name__)
#         return (doctest.testmod(pkg, *args, **kwargs),) + tuple(
#         _doctest_recursively(p) for p in dir(pkg))
# doctest.testmod(pkg, verbose=True)''' % pkg
    cmd = 'import doctest, %s as pkg; doctest.testmod(pkg, verbose=True)' % pkg
    return _python('-c "%s"' % cmd, level=INFO, venv=venv)


def cleanup(test_dir=TEST_PATH):
    """remove temporary files"""
    log(INFO, ICONS["clean"] + 'clean test results')
    # removed pytest data files
    del_tree(".pytest_cache")
    return 0
