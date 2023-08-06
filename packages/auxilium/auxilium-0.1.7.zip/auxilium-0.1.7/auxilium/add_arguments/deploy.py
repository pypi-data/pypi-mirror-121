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

from auxilium.tools.git_tools import push_git
from auxilium.tools.build_tools import build, cleanup as cleanup_build
from auxilium.tools.docmaintain_tools import docmaintain, \
    get_version, get_url, get_author
from auxilium.tools.pypi_tools import deploy


def add_arguments(parser=None, config=ConfigParser()):
    parser = ArgumentParser() if parser is None else parser
    parser.add_argument(
        '--header',
        action='store_const',
        const=not config.getboolean('deployment', 'header', fallback=True),
        default=config.getboolean('deployment', 'header', fallback=True),
        help=docmaintain.__doc__)
    parser.add_argument(
        '--build',
        action='store_const',
        const=not config.getboolean('deploy', 'build', fallback=True),
        default=config.getboolean('deploy', 'build', fallback=True),
        help=build.__doc__)
    parser.add_argument(
        '--commit',
        nargs='?',
        const=config.get('deploy', 'commit', fallback='commit build'),
        help='auto commit on successful build')
    ver = 'v' + get_version()
    parser.add_argument(
        '--tag',
        nargs='?',
        const=config.getboolean('deploy', 'tag', fallback=ver),
        help='auto tag on successful build')
    parser.add_argument(
        '--push',
        action='store_const',
        const=not config.getboolean('deploy', 'push', fallback=False),
        default=config.getboolean('deploy', 'push', fallback=False),
        help=push_git.__doc__ + ' - requires REMOTE')
    parser.add_argument(
        '--remote',
        default=config.get('deploy', 'remote', fallback=get_url()),
        help='remote `git` repo')
    parser.add_argument(
        '--remote_usr',
        metavar='USR',
        default=config.get('deploy', 'remote_usr', fallback=get_author()),
        help='user on remote `git` repo')
    parser.add_argument(
        '--remote_pwd',
        metavar='PWD',
        default=config.get('deploy', 'remote_pwd', fallback='None'),
        help='password/token on remote `git` repo')
    parser.add_argument(
        '--deploy',
        action='store_const',
        const=not config.getboolean('deploy', 'deploy', fallback=False),
        default=config.getboolean('deploy', 'deploy', fallback=False),
        help=deploy.__doc__ + ' - requires USR and PWD')
    parser.add_argument(
        '--pypi_usr',
        metavar='USR',
        default=config.get('deploy', 'pypi_usr', fallback='None'),
        help='user on `pypi.org`')
    parser.add_argument(
        '--pypi_pwd',
        metavar='PWD',
        default=config.get('deploy', 'pypi_pwd', fallback='None'),
        help='password/token on `pypi.org`')
    parser.add_argument(
        '--cleanup',
        action='store_const',
        const=not config.getboolean('deploy', 'cleanup', fallback=False),
        default=config.getboolean('deploy', 'cleanup', fallback=False),
        help=cleanup_build.__doc__)
    return parser
