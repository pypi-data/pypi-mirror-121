# -*- coding: utf-8 -*-

# auxilium
# --------
# Python project for an automated test and deploy toolkit.
#
# Author:   sonntagsgesicht
# Version:  0.1.7, copyright Thursday, 30 September 2021
# Website:  https://github.com/sonntagsgesicht/auxilium
# License:  Apache License 2.0 (see LICENSE file)


from argparse import ArgumentParser
from configparser import ConfigParser

from auxilium.tools.test_tools import cleanup as cleanup_test
from auxilium.tools.security_tools import security
from auxilium.tools.quality_tools import quality
from auxilium.tools.coverage_tools import coverage

from auxilium.tools.const import TEST_PATH


def add_arguments(parser=None, config=ConfigParser()):
    parser = ArgumentParser() if parser is None else parser
    parser.add_argument(
        'path',
        nargs='?',
        default=config.get('test', 'path', fallback=TEST_PATH),
        help='path to directory where test are found')
    parser.add_argument(
        '--commit',
        nargs='?',
        const=config.get('test', 'commit', fallback='commit tested'),
        help='auto commit on successful test run')
    parser.add_argument(
        '--coverage',
        action='store_const',
        const=not config.getboolean('test', 'coverage', fallback=True),
        default=config.getboolean('test', 'coverage', fallback=True),
        help=coverage.__doc__)
    parser.add_argument(
        '--quality',
        action='store_const',
        const=not config.getboolean('test', 'quality', fallback=True),
        default=config.getboolean('test', 'quality', fallback=True),
        help=quality.__doc__)
    parser.add_argument(
        '--security',
        action='store_const',
        const=not config.getboolean('test', 'security', fallback=True),
        default=config.getboolean('test', 'security', fallback=True),
        help=security.__doc__)
    parser.add_argument(
        '--cleanup',
        action='store_const',
        const=not config.getboolean('test', 'cleanup', fallback=False),
        default=config.getboolean('test', 'cleanup', fallback=False),
        help=cleanup_test.__doc__)
    return parser
