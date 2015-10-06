#! /usr/bin/env python

import os
import sys
import argparse
import urlparse
import subprocess


def main(args=sys.argv[1:]):
    """
    Yet Another GitHub URL tool - produce public URLs from local paths.
    """
    opts = parse_args(args)
    urlish = get_remote_urlish(opts.LOCALPATH, opts.REMOTE)
    url = patch_git_urlish(urlish)
    urlp = urlparse.urlparse(url)
    raise NotImplementedError(urlp)


def parse_args(args):
    p = argparse.ArgumentParser(description=main.__doc__)

    p.add_argument('-m', '--mode',
                   dest='MODE',
                   default='commit',
                   choices=['commit', 'branch', 'both'],
                   help='Show a commit or branch specific URL, or show both.')

    p.add_argument('-r', '--remote',
                   dest='REMOTE',
                   default=None,
                   help=('The remote to link to; if absent pick the first '
                         + 'match from git remote -v'))

    p.add_argument('LOCALPATH',
                   help='Local path within a git repo with a github remote.')

    p.add_argument('LINE',
                   type=int,
                   nargs='?',
                   help='Line number (or starting line).')

    p.add_argument('ENDLINE',
                   type=int,
                   nargs='?',
                   help='Ending line for a range URL.')

    return p.parse_args(args)


def get_remote_urlish(path, remotename):
    output = subprocess.check_output(
        ['git', 'remote', '-v'],
        cwd=os.path.dirname(path))

    for line in output.splitlines():
        [name, urlish, kind] = line.split()
        if kind == '(fetch)':
            if remotename is None:
                return urlish
            elif name == remotename:
                return urlish
        else:
            assert kind == '(push)', 'unknown remote kind: {}'.format(kind)

    assert False, 'remote {} not found.'.format(remotename)


def patch_git_urlish(urlish):
    PREFIX = 'git@github.com:'
    SUFFIX = '.git'
    if urlish.startswith(PREFIX):
        assert urlish.endswith(SUFFIX), repr(urlish)
        guts = urlish[len(PREFIX):-len(SUFFIX)]
        return 'https://github.com/' + guts
    else:
        return urlish


if __name__ == '__main__':
    main()
