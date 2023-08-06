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

from auxilium.tools.sphinx_tools import api, html, doctest, show, \
    cleanup as cleanup_doc


def add_arguments(parser=None, config=ConfigParser()):
    parser = ArgumentParser() if parser is None else parser
    parser.add_argument(
        '--commit',
        nargs='?',
        const=config.get('doc', 'commit', fallback='commit docs'),
        help='auto commit on successful doc build run')
    parser.add_argument(
        '--api',
        action='store_const',
        const=not config.getboolean('doc', 'api', fallback=False),
        default=config.getboolean('doc', 'api', fallback=False),
        help=api.__doc__)
    parser.add_argument(
        '--doctest',
        action='store_const',
        const=not config.getboolean('doc', 'doctest', fallback=True),
        default=config.getboolean('doc', 'doctest', fallback=True),
        help=doctest.__doc__)
    parser.add_argument(
        '--html',
        action='store_const',
        const=not config.getboolean('doc', 'doctest', fallback=True),
        default=config.getboolean('doc', 'doctest', fallback=True),
        help=html.__doc__)
    # parser.add_argument(
    #     '--latexpdf',
    #     action='store_const',
    #     const=not config.getboolean('doc', 'latexpdf', fallback=False),
    #     default=config.getboolean('doc', 'latexpdf', fallback=False),
    #     help=latexpdf.__doc__)
    parser.add_argument(
        '--show',
        action='store_const',
        const=not config.getboolean('doc', 'show', fallback=False),
        default=config.getboolean('doc', 'show', fallback=False),
        help=show.__doc__)
    parser.add_argument(
        '--cleanup',
        action='store_const',
        const=not config.getboolean('doc', 'cleanup', fallback=False),
        default=config.getboolean('doc', 'cleanup', fallback=False),
        help=cleanup_doc.__doc__)
    return parser
