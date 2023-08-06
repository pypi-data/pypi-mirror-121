# -*- coding: utf-8 -*-

# auxilium
# --------
# Python project for an automated test and deploy toolkit.
#
# Author:   sonntagsgesicht
# Version:  0.1.7, copyright Thursday, 30 September 2021
# Website:  https://github.com/sonntagsgesicht/auxilium
# License:  Apache License 2.0 (see LICENSE file)


from os import getcwd
from os.path import basename

from ..tools.pip_tools import upgrade as _upgrade, uninstall, \
    cleanup as _cleanup, requirements as _requirements, install as _install
from ..tools.git_tools import commit_git
from ..tools.docmaintain_tools import docmaintain


def do(pkg=basename(getcwd()), commit=None, add=None, upgrade=None,
       install=None, requirements=None, header=None, cleanup=None,
       path=getcwd(), env=None, **kwargs):

    if cleanup:
        code = _cleanup(path=path, venv=env)
        return code or uninstall(pkg, venv=env)

    code = False

    if upgrade:
        code = code or _upgrade(upgrade, path=path, venv=env)

    if install:
        code = code or _install(path=path, venv=env)

    if requirements:
        code = code or _requirements(path=path, venv=env)

    if header:
        code = code or docmaintain(pkg, path=path)

    if commit:
        code = code or commit_git(commit, path=path)

    return code
