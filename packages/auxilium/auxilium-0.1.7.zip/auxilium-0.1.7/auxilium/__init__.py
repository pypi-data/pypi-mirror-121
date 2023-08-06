# -*- coding: utf-8 -*-

# auxilium
# --------
# Python project for an automated test and deploy toolkit.
#
# Author:   sonntagsgesicht
# Version:  0.1.7, copyright Friday, 01 October 2021
# Website:  https://github.com/sonntagsgesicht/auxilium
# License:  Apache License 2.0 (see LICENSE file)


import logging

from .rst_tools import replacements_str, replacements_from_pkg, \
    replacements_from_cls, replacements  # noqa: F401

logging.getLogger(__name__).addHandler(logging.NullHandler())

__doc__ = 'Python project for an automated test and deploy toolkit.'
__version__ = '0.1.7'
__dev_status__ = '4 - Beta'
__date__ = 'Friday, 01 October 2021'
__author__ = 'sonntagsgesicht'
__email__ = __author__ + '@icloud.com'
__url__ = 'https://github.com/' + __author__ + '/' + __name__
__license__ = 'Apache License 2.0'
__dependencies__ = 'pip', 'dulwich', 'flake8', 'bandit', 'coverage', \
                   'sphinx', 'sphinx_rtd_theme', 'sphinx_math_dollar', \
                   'twine',
__dependency_links__ = ()
__data__ = ('data/pkg.zip',)
__scripts__ = ('auxilium/scripts/auxilium',)


# todo: make full run before deploy new release:
#  install->maintain->test->doc->build->commit->tag->push->deploy->release
#  and separate build from deploy module incl. --test option

# todo: add -ff --fail-fast option

# todo: capture log in shell in case of an error
