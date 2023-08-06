# -*- coding: utf-8 -*-

# auxilium
# --------
# Python project for an automated test and deploy toolkit.
#
# Author:   sonntagsgesicht
# Version:  0.1.7, copyright Thursday, 30 September 2021
# Website:  https://github.com/sonntagsgesicht/auxilium
# License:  Apache License 2.0 (see LICENSE file)


from logging import log, INFO, WARN
from os import remove, getcwd
from os.path import basename, exists, join

from auxilium.tools.const import ICONS
from auxilium.tools.system_tools import module, del_tree

FREEZE_FILE = '.freeze'
TEMP_REMOVE_FILE = '.site_packages_to_remove'
PIP = 'pip'


def upgrade(pkg=PIP, path=getcwd(), venv=None):
    """upgrade python library [PKG] via `pip`"""
    log(INFO, ICONS["upgrade"] + 'upgrade `%s`' % pkg)
    return module(PIP, 'install --upgrade %s' % pkg, path=path, venv=venv)


def requirements(path=getcwd(), venv=None):
    """manage requirements (dependencies) in `requirements.txt`
        and `upgrade_requirements.txt`"""
    log(INFO, ICONS["setup"] + "setup environment requirements")

    res = 0
    if not exists(join(path, FREEZE_FILE)):
        res += module(PIP, "freeze > %s" % FREEZE_FILE, path=path, venv=venv)

    if exists(join(path, "requirements.txt")):
        res += module(PIP, "install -r requirements.txt",
                      path=path, venv=venv)

    if exists(join(path, "upgrade_requirements.txt")):
        res += module(PIP, "install --upgrade -r upgrade_requirements.txt",
                      path=path, venv=venv)
    return res


def install(path=getcwd(), venv=None):
    """(re)install current project via `pip install -e .`"""
    log(INFO, ICONS["install"] + 'install project via pip install -e')
    if exists('setup.py') or exists('setup.cfg'):
        return module(PIP, "install --upgrade -e .", path=path, venv=venv)
    log(WARN, ICONS["warn"] +
        'could not install project via pip install -e '
        '(setup.py or setup.cfg not found in %s)' % path)
    return 1


def uninstall(pkg=basename(getcwd()), path=getcwd(), venv=None):
    """uninstall current project via `pip uninstall`"""
    log(INFO, ICONS["uninstall"] + 'uninstall project via pip uninstall')
    return module(PIP, "uninstall -y %s" % pkg, path=path, venv=venv)


def cleanup(path=getcwd(), venv=None):
    """remove temporary files"""
    log(INFO, ICONS["clean"] + 'clean environment')
    res = 0
    if exists(join(path, FREEZE_FILE)):
        res += module(PIP, "freeze --exclude-editable > %s" % TEMP_REMOVE_FILE,
                      path=path, venv=venv)
        res += module(PIP, "uninstall -r %s -y" % TEMP_REMOVE_FILE,
                      path=path, venv=venv)
        remove(TEMP_REMOVE_FILE)

        res += module(PIP, "install --upgrade -r %s" % FREEZE_FILE,
                      path=path, venv=venv)
        remove(join(path, FREEZE_FILE))
    res += del_tree(basename(path) + ".egg-info", ".eggs")
    return res
