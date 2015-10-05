#! /usr/bin/env python

import sys
import argparse


def main(args=sys.argv[1:]):
    """
    Yet Another GitHub URL tool - produce public URLs from local paths.
    """
    opts = parse_args(args)
    raise NotImplementedError(opts)


def parse_args(args):
    p = argparse.ArgumentParser(description=main.__doc__)

    p.add_argument('-r', '--referent',
                   dest='referent',
                   default='commit',
                   choices=['commit', 'branch', 'both'],
                   help='Show a commit or branch specific URL, or show both.')

    p.add_argument('LOCALPATH',
                   help='Local path within a git repo with a github remote.')

    p.add_argument('LINE',
                   nargs='?',
                   help='Line number (or starting line).')

    p.add_argument('ENDLINE',
                   nargs='?',
                   help='Ending line for a range URL.')

    return p.parse_args(args)


if __name__ == '__main__':
    main()
