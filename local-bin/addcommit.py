#!/usr/bin/env python

import argparse
import shutil
import sys
import subprocess

git_cmd = shutil.which('git')

def arguments(argv=None):
    parser = argparse.ArgumentParser(description="A wrapper to combine git-add & git-commit")
    parser.add_argument('-v', '--verbose', action='store_true', help='Show each command run')
    # add
    parser.add_argument('--dry-run', action='store_true', help="Don't do anything for real")
    parser.add_argument('-f', '--force-add', action='store_true', help="Force add to the index")
    # commit
    parser.add_argument('-i', '--interactive', action='store_true', help="Do add-commit interactively")
    parser.add_argument('-m', type=str, help='Commit message')
    parser.add_argument('-n', '--no-commit', action='store_true', help='Do not commit changes')
    parser.add_argument('pathspec', nargs='*')

    if argv is None:
        return parser.parse_args()
    return parser.parse_args(argv)

def run(cmd, error_message=None, verbose=False):
    """ Run a command with in subprocess """
    if verbose:
        print(f"subprocess.run: {' '.join(cmd)}")

    result = subprocess.run(cmd)

    if result.returncode != 0:
        if error_message is None:
            error_message = f"Failed to execute {cmd}"

        print(error_message, file=sys.stderr)
        sys.exit(1)


def add(args):
    """ Add pathspec to staged """
    if len(args.pathspec) <= 0:
        print('No items to add were given', file=sys.stderr)
        sys.exit(1)

    extra = []
    if args.force_add:
        extra.append('--force')

    run([git_cmd, 'add', *extra, *args.pathspec], verbose=args.verbose)

def commit(args):
    """ Create a commit """
    if args.no_commit:
        print('No commit requested !!', file=sys.stderr)
    elif args.m:
        run([git_cmd, 'commit', '-m', f"'{args.m}'"], verbose=args.verbose)
    else:
        run([git_cmd, 'commit'], verbose=args.verbose)


def main(args):
    """ Run addcommit """

    if args.dry_run:
        for item in args.pathspec:
            print(f'adding {item}')

        if args.m:
            print(f'commit-message: {args.m}')
        sys.exit(0)

    if args.interactive:
        run([git_cmd, 'commit', '--interactive'])
    else:
        add(args)
        commit(args)


if __name__ == '__main__':
    if not git_cmd:
        print('GIT: is not installed on this system', file=sys.stderr)
        sys.exit(1)

    _args = arguments()
    print(_args)
    main(_args)