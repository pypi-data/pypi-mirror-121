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
from logging import log, ERROR

from ..tools.const import ICONS
from ..tools.coverage_tools import coverage as _coverage, \
    cleanup as cleanup_coverage
from ..tools.git_tools import commit_git
from ..tools.quality_tools import quality as _quality
from ..tools.security_tools import security as _security
from ..tools.test_tools import test as _test, cleanup as cleanup_test


def do(pkg=basename(getcwd()), commit=None,
       quality=None, security=None, coverage=None, cleanup=None,
       path=None, env=None, **kwargs):
    """run test process"""

    if cleanup:
        return cleanup_test(path) or cleanup_coverage(path)

    test_return_code = -1
    code = False

    if quality:
        code = code or _quality(pkg, venv=env)

    if security:
        code = code or _security(pkg, venv=env)

    if path:
        test_return_code = _test(path, venv=env)
        code = code or test_return_code

    if coverage and path:
        code = code or _coverage(pkg, path, venv=env)

    if commit:
        if test_return_code == 0:
            code = code or commit_git(commit)
        else:
            log(ERROR, ICONS["error"] +
                'Test missing or failed . did not commit.')

    return code
