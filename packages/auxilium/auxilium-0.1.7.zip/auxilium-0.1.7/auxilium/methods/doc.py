# -*- coding: utf-8 -*-

# auxilium
# --------
# Python project for an automated test and deploy toolkit.
#
# Author:   sonntagsgesicht
# Version:  0.1.7, copyright Thursday, 30 September 2021
# Website:  https://github.com/sonntagsgesicht/auxilium
# License:  Apache License 2.0 (see LICENSE file)


from logging import log, ERROR
from os import getcwd
from os.path import basename

from ..tools.git_tools import commit_git
from ..tools.const import ICONS
from ..tools.sphinx_tools import api as _api, doctest as _doctest, \
    html as _html, show as _show, cleanup as _cleanup


def do(pkg=basename(getcwd()), commit=None,
       api=None, doctest=None, html=None, show=None, cleanup=None,
       path=None, env=None, **kwargs):
    if cleanup:
        return _cleanup(env)

    doctest_return_code = html_return_code = -1
    code = False
    if api:
        code = code or _cleanup(env)
        code = code or _api(pkg, env)
    if doctest:
        doctest_return_code = _doctest(env)
        code = code or doctest_return_code
    if html:
        html_return_code = _html(env)
        code = code or html_return_code
    if show:
        _show(env)
    if commit:
        if doctest_return_code == 0 and html_return_code == 0:
            code = code or commit_git(commit)
        else:
            log(ERROR, ICONS["error"] +
                'doctest or build missing or failed . did not commit.')
    return code
