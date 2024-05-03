#!/usr/bin/env python3
import itertools
import sys
import re
import argparse
import warnings
from pathlib import Path
from typing import Optional, List

try:
    from rich.console import Console
    from rich.tree import Tree
except ImportError:
    # if rich is not installed try using rich bundled with pip
    # this is a little bit of cheating with dependencies but should be ok
    try:
        from pip._vendor.rich.console import Console
        from pip._vendor.rich.tree import Tree
    except ImportError:
        print('Error: Failed to load dependencies !!!')
        print('You are using a version of python that is inferion than 3.7 or a version of pip inferion to 22.0',
              file=sys.stderr)
        print('Try upgrading pip or your python version, or install the rich library')
        sys.exit(1)

error_console = Console(stderr=True, style="bold red")
std_console = Console()


def get_file_icon(filename: str) -> str:
    """ Return icon corresponding to file type """
    suffix = Path(filename).suffix
    if suffix == ".py":
        return "🐍"
    # todo find more icons
    else:
        return "📄"


def parse_args(argv=None):
    """ Parsing arguments """
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(description="List files & directories in a tree like structure.")
    parser.add_argument('dirname')
    parser.add_argument('-L', '--max-depth', default=None, help="maximum depth")
    parser.add_argument('-i', '--include', nargs="*", default=[], help="patterns to include files [can be any pattern]")
    parser.add_argument('-e', '--exclude', nargs="*", default=[], help="patterns to exclude files [must be valid python regexp]")
    parser.add_argument('-d', '--exclude-dir', nargs="*", default=[], help="patterns to exclude dirs [must be valid python regexp]")

    return parser.parse_args(argv)


def filter_files_gen(files_loc: Path, include: Optional[List[str]] = None, exclude: Optional[List[str]] = None):
    """ Creates a generator of the files present in files_loc (allow usage of include/exclude regex list"""
    if include is not None and len(include) > 0:
        files = itertools.chain(*[files_loc.glob(pt) for pt in include])
    else:
        files = files_loc.glob("*")

    if exclude is not None and len(exclude) > 0:
        for rgx in exclude:
            try:
                pt = re.compile(rgx)
                files = filter(lambda x: not pt.match(x.name), files)
            except re.error:
                warnings.warn(f"Failed to compile {rgx} not a valid python regex")

    for f in files:
        if f.is_file():
            yield f


def add_children(
        location: Path, root_node,
        pattern_include: Optional[List[str]] = None,
        pattern_exclude: Optional[List[str]] = None,
        excluded_dirs: Optional[List[str]] = None,
        depth: int = 0, max_depth: Optional[int] = None,
):
    """ Add children to node """
    items = [i for i in location.iterdir()]
    folders = [i for i in items if i.is_dir()]

    if excluded_dirs:
        excluded_dirs = set(excluded_dirs)
    else:
        excluded_dirs = set([])

    if max_depth is not None and depth >= max_depth:
        return

    for cur_dir in folders:
        # skip for any excluded dir
        if cur_dir.name in excluded_dirs:
            continue

        folder_node = root_node.add(f":file_folder: {cur_dir.name}/")
        add_children(
            cur_dir, folder_node,
            depth=depth + 1, pattern_include=pattern_include,
            pattern_exclude=pattern_exclude, max_depth=max_depth
        )

    # add all files after filtering
    for f in filter_files_gen(location, include=pattern_include, exclude=pattern_exclude):
        root_node.add(f"{get_file_icon(f.name)} {f.name}")


def tree_cmd(argv=None):
    args = parse_args(argv)
    
    root_dir = Path(args.dirname)
    max_depth = args.max_depth
    if max_depth:
        max_depth = int(max_depth)

    if not root_dir.is_dir():
        error_console.print(f'{root_dir} is not a directory or does not exist !!!')
        sys.exit(1)

    root_node = Tree(f":file_folder: {root_dir.resolve().name}", highlight=True)
    add_children(
        root_dir, root_node, max_depth=max_depth, 
        pattern_include=args.include, pattern_exclude=args.exclude,
        excluded_dirs=args.exclude_dir
    )

    std_console.print(root_node)


if __name__ == "__main__":
    tree_cmd()
