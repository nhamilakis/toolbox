#!/usr/bin/env python3
import shlex
import shutil
import subprocess
import argparse
import sys
from pathlib import Path

PY_VERSION_DIR = Path.home() / ".local/lib/pyenv/versions"
DRY_RUN: bool = False


def execute(cmd: str, fail_ok: bool = False, transparency: bool = True):
    """Execute a system command and capture its output"""
    if DRY_RUN:
        print(f"$> {cmd}")
        return 0, ""

    cmd_list = shlex.split(cmd)
    exec_path = shutil.which(cmd_list[0])
    if not exec_path:
        raise EnvironmentError(f"Command {cmd_list[0]} was not found on system")

    cmd_list[0] = exec_path
    if transparency:
        subprocess.run(cmd_list)
    else:
        result = subprocess.run(cmd_list, capture_output=True)

        if result.returncode == 0:
            return result.returncode, result.stdout.decode()
        return result.returncode, result.stderr.decode()


def python(pyenv_path, cmd):
    """ Execute a python command with a given environment """
    py_path = pyenv_path / "bin" / "python"
    if not py_path.is_file():
        raise FileNotFoundError(f"ERROR: {pyenv_path} is not a python environment")

    return execute(f"{py_path} {cmd}")


def get_all_pyenvs():
    """ Return all environments in pyenv dir """
    return [p for p in PY_VERSION_DIR.iterdir() if p.is_dir()]


def update_in_all(pkg_name):
    """ Upgrade all packages in all the environments """
    for path in get_all_pyenvs():
        python(path, f"-m pip install --upgrade {pkg_name}")


class CMDParser:
    """Object to parse command line arguments"""

    def __init__(self, argv=None):
        argv = argv if argv else sys.argv[1:]

        parser = argparse.ArgumentParser(
            description="Run batch commands in all pyenv environments",
            usage="""py-run.py <command> [<args>]
            
    The most commonly used subcommand are: 
        update_pkg A tool to update all package instances in all existing environments.
"""
        )
        parser.add_argument("command", help="Subcommand to run")
        args = parser.parse_args([argv[0]])

        if not hasattr(self, args.command):
            print("Unrecognized command", file=sys.stderr)
            parser.print_help()
            sys.exit(1)

        getattr(self, args.command)(argv[1:])

    def update_pkg(self, argv):
        parser = argparse.ArgumentParser(description='Update a pip package in all environments')
        parser.add_argument('pkg_name', type=str)
        args = parser.parse_args(argv)
        # update in all envs
        update_in_all(args.pkg_name)


if __name__ == "__main__":
    CMDParser()
