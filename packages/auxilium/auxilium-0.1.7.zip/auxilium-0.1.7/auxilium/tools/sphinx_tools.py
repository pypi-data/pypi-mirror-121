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
from os import getcwd, name as os_name
from os.path import exists, basename, normpath, join
from shutil import rmtree

from .const import ICONS
from .system_tools import shell

SPHINX_API_PATH = normpath("doc/sphinx/api")
SPHINX_INDEX_FILE = normpath("./doc/sphinx/_build/html/intro.html")
SPHINX_PATH = normpath("./doc/sphinx/")

SPHINX_BUILD_PATH = normpath("./doc/sphinx/_build")
SPHINX_BUILD_HTML_PATH = normpath("./doc/sphinx/_build/html")
SPHINX_BUILD_LATEX_PATH = normpath("./doc/sphinx/_build/latex")

SPHINX_BUILD_PATHS = SPHINX_PATH, SPHINX_BUILD_PATH
SPHINX_HTML_PATHS = SPHINX_PATH, SPHINX_BUILD_HTML_PATH
SPHINX_LATEX_PATHS = SPHINX_PATH, SPHINX_BUILD_LATEX_PATH


def api(pkg=basename(getcwd()), venv=None):
    """add api entries to `sphinx` docs"""
    log(INFO, ICONS["commit"] + 'run sphinx apidoc scripts')
    if exists(SPHINX_API_PATH):
        rmtree(SPHINX_API_PATH)
    res = 0
    cmd = "sphinx-apidoc -o %s -f -E %s" % (SPHINX_API_PATH, pkg)
    res += shell(cmd, venv=venv)
    return res


def html(venv=None):
    """build html documentation (using `sphinx`)"""
    # cleanup(venv)
    # if not exists(SPHINX_API_PATH):
    #     api(venv=venv)
    log(INFO, ICONS["html"] +
        'run sphinx html scripts (only on new or modified files)')
    return shell(
        "sphinx-build -W --keep-going -b html %s %s" % SPHINX_HTML_PATHS,
        venv=venv)


def latexpdf(venv=None):
    """build pdf documentation (using `sphinx` and `LaTeX`)"""
    log(INFO, ICONS["latexpdf"] +
        'run sphinx latexpdf scripts (only on new or modified files)')
    return shell(
        "sphinx-build -M latexpdf -W --keep-going %s %s" % SPHINX_LATEX_PATHS,
        venv=venv)


def doctest(venv=None):
    """run `sphinx` doctest"""
    log(INFO, ICONS["doctest"] +
        'run sphinx doctest scripts (only on new or modified files)')
    return shell(
        "sphinx-build -W --keep-going -b doctest %s %s " % SPHINX_BUILD_PATHS,
        venv=venv)


def show(venv=None):
    """show html documentation"""
    log(INFO, ICONS["show"] +
        'find docs at %s' % join(getcwd(), SPHINX_INDEX_FILE))
    if os_name == 'posix':
        return shell("open %s" % SPHINX_INDEX_FILE, venv=venv)
    if os_name == 'nt':
        return shell("start %s" % SPHINX_INDEX_FILE, venv=venv)
    return 1


def cleanup(venv=None):
    """remove temporary files"""
    log(INFO, ICONS["clean"] + 'clean environment')
    return shell("sphinx-build -M clean %s %s" % SPHINX_BUILD_PATHS,
                 venv=venv)
