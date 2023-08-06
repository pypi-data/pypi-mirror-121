# -*- coding: utf-8 -*-

# auxilium
# --------
# Python project for an automated test and deploy toolkit.
#
# Author:   sonntagsgesicht
# Version:  0.1.7, copyright Thursday, 30 September 2021
# Website:  https://github.com/sonntagsgesicht/auxilium
# License:  Apache License 2.0 (see LICENSE file)


import logging
import pathlib
import sys
import os

from argparse import ArgumentParser
from configparser import ConfigParser

from auxilium.add_arguments import ArgumentDefaultsAndConstsHelpFormatter
from auxilium.tools.const import CONFIG_PATH, DEMO_PATH, VERBOSITY_LEVELS, \
    ICONS
from auxilium.tools.setup_tools import create_project
from auxilium.tools.system_tools import module, del_tree
from auxilium import add_arguments, methods

Failure = Exception


def main():
    # ==========================
    # === init config parser ===
    # ==========================

    config = ConfigParser(allow_no_value=True)
    config.read(pathlib.Path.home().joinpath(CONFIG_PATH))
    config.read(CONFIG_PATH)

    if not config.getboolean('DEFAULT', 'icons', fallback=os.name == 'posix'):
        ICONS.clear()
        ICONS.update({'error': '!!', 'warn': '!'})

    # ===========================
    # === add argument parser ===
    # ===========================

    epilog = \
        "if (default: True) a given flag turns its value to False. " + \
        "default behavior may depend on current path and project. " + \
        "set default behavior in `~/%s` and `./%s`." % \
        (CONFIG_PATH, CONFIG_PATH)

    parser = ArgumentParser(
        epilog=epilog, formatter_class=ArgumentDefaultsAndConstsHelpFormatter)

    sub_parser = parser.add_subparsers(dest='command')

    # === create ===
    sub_parser.add_parser(
        'create',
        epilog=epilog,
        formatter_class=ArgumentDefaultsAndConstsHelpFormatter,
        help=create_project.__doc__)

    # === update ===
    sub_parser.add_parser(
        'update',
        epilog=epilog,
        formatter_class=ArgumentDefaultsAndConstsHelpFormatter,
        help="keep project, repo and dependencies up-to-date")

    # === test ==
    sub_parser.add_parser(
        'test',
        epilog=epilog,
        formatter_class=ArgumentDefaultsAndConstsHelpFormatter,
        help="check project integrity by testing using `pytest`")

    # === documentation ==
    sub_parser.add_parser(
        'doc',
        epilog=epilog,
        formatter_class=ArgumentDefaultsAndConstsHelpFormatter,
        help="update project documentation using `sphinx`")

    # === deploy ==
    sub_parser.add_parser(
        'deploy',
        epilog=epilog,
        formatter_class=ArgumentDefaultsAndConstsHelpFormatter,
        help="manage project deployment")

    # === invoke python ==
    sub_parser.add_parser(
        'python',
        epilog='Call python interpreter of virtual environment '
               '(Note: only some options are implemented)',
        formatter_class=ArgumentDefaultsAndConstsHelpFormatter,
        help="invoke (virtual environment) python")

    # ===============================
    # === add arguments to parser ===
    # ===============================

    method = getattr(add_arguments, 'root', None)
    method(parser, config) if method else None

    for k, v in sub_parser.choices.items():
        method = getattr(add_arguments, k, None)
        method(v, config) if method else None

    # ===============================
    # === invoke parsed arguments ===
    # ===============================

    args = parser.parse_args()

    verbosity, formatter = VERBOSITY_LEVELS[
        min(args.verbosity, len(VERBOSITY_LEVELS) - 1)]
    logging.basicConfig(level=verbosity, format=formatter)
    logging.log(1, args)

    # check virtual environment
    if args.env \
            and not os.path.exists(args.env) \
            and args.command != 'create' \
            and not args.demo:
        msg = ICONS["warn"] + \
              'did not find a virtual environment at %s. ' % args.env
        logging.log(logging.WARN, msg)
        msg = ICONS[""] + \
            'consider creating one with ' \
            '`auxilium create --update --venv=[PATH]` ' \
            'or use an `-e= ` argument'
        logging.log(logging.WARN, msg)
        sys.exit(1)

    # check demo
    if args.demo:
        logging.log(logging.INFO, ICONS["demo"] + 'starting demo - relax')

        del_tree(DEMO_PATH)
        v = '-' + 'v' * args.verbosity if args.verbosity else ''
        z = '-' + 'x' * args.exit_status if args.exit_status else ''
        e = '-e=' + args.env
        cmd = (' %s %s %s create '
               '--name=%s '
               '--slogan="a demo by auxilium" '
               '--author=auxilium '
               '--email="sonntagsgesicht@icould.com" '
               '--url="https://github.com/sonntagsgesicht/auxilium"') % \
              (v, z, e, DEMO_PATH)
        sys.exit(module('auxilium', cmd, level=logging.INFO))

    # check command
    method = getattr(methods, str(args.command), None)
    if method is None:
        print('>>> auxilium -h')
        parser.print_help()
        for key, choice in sub_parser.choices.items():
            print('\n>>> auxilium ' + key + ' -h')
            choice.print_help()
        sys.exit()

    path = os.getcwd()
    pkg = os.path.basename(os.getcwd())
    full_path = os.path.join(path, pkg)

    if not os.path.exists(full_path) \
            and args.command not in ('create', 'python'):
        msg = ICONS["warn"] + \
              'no maintainable project found at %s ' % full_path
        logging.log(logging.WARN, msg)
        msg = ICONS[""] + \
            'consider creating one with `auxilium create` ' \
            '(or did you mean `auxilium python`?)'
        logging.log(logging.WARN, msg)
        sys.exit(1)

    kwargs = vars(args)
    kwargs['path'] = kwargs.get('path', path)
    kwargs['pkg'] = kwargs.get('name', pkg)

    if path not in sys.path:
        sys.path.append(path)

    code = method(**kwargs) if method else 1
    if code:
        msg = 'non-zero exit status (failure in `%s`)' % args.command
        logging.log(logging.ERROR, ICONS['error'] + msg)
        if args.exit_status > 2:
            raise Failure(msg)
        if args.exit_status == 2:
            sys.exit(1)
        if args.exit_status == 1:
            sys.exit(0)
        if args.exit_status == 0:
            sys.exit(1)
    sys.exit()


if __name__ == '__main__':
    main()
