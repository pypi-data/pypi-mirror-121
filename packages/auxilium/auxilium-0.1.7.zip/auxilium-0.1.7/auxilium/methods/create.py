# -*- coding: utf-8 -*-

# auxilium
# --------
# Python project for an automated test and deploy toolkit.
#
# Author:   sonntagsgesicht
# Version:  0.1.7, copyright Thursday, 30 September 2021
# Website:  https://github.com/sonntagsgesicht/auxilium
# License:  Apache License 2.0 (see LICENSE file)


from os import getcwd, chdir
from os.path import basename, join
from sys import path as sys_path

from ..tools.setup_tools import create_project, create_finish
from ..tools.system_tools import create_venv, del_tree
from ..tools.git_tools import commit_git
from ..tools.pip_tools import upgrade, install, requirements
from ..tools.docmaintain_tools import docmaintain


def do(name=None, slogan=None, author=None, email=None, url=None,
       commit=None, path=getcwd(), venv=None, update=None, env=None,
       **kwargs):
    if update:
        project_path = join(path, name) if name else path
        pkg = basename(project_path)
        code = 0
    else:
        # creat project
        project_path = \
            create_project(name, slogan, author, email, url, path=path)
        pkg = basename(project_path)
        code = int(not project_path.endswith(name)) if name else 0

        chdir(project_path)
        sys_path.append(project_path)
        code = code or docmaintain(pkg, path=project_path)
        if commit:
            # init git repo with initial commit
            code = code or commit_git(commit, path=project_path)

    if venv:
        chdir(project_path)
        # create virtual environment
        # venv = venv.replace('bin/python3')
        del_tree(venv)
        env = create_venv(pkg, venv_path=venv, path=project_path, venv=env)

        # run default update command
        code = code or upgrade(path=project_path, venv=env)
        code = code or install(path=project_path, venv=env)
        code = code or requirements(path=project_path, venv=env)

    if not update:
        code = code or create_finish(pkg)
    return code
