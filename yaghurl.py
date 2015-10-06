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
    (urlish, relpath, branch, commit) = get_git_info(opts.LOCALPATH, opts.REMOTE)
    (branchurl, commiturl) = calculate_urls(urlish, relpath, branch, commit)

    displayfunc = globals()['display_' + opts.FORMAT]
    displayfunc(sys.stdout, opts.MODE, relpath, branch, branchurl, commit, commiturl)


def parse_args(args):
    p = argparse.ArgumentParser(description=main.__doc__)

    p.add_argument('-m', '--mode',
                   dest='MODE',
                   default='commit',
                   choices=['commit', 'branch', 'both'],
                   help='Show a commit or branch specific URL, or show both.')

    p.add_argument('-f', '--format',
                   dest='FORMAT',
                   default='bare',
                   choices=['bare', 'comment'],
                   help=('Display the results in a bare (plain text) or '
                         + 'github-style comment format.'))

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


def get_git_info(path, remotename):
    git = GitCmd(path)
    urlish = get_remote_urlish(git, remotename)
    branch = git('rev-parse', '--abbrev-ref', 'HEAD').strip()
    commit = git('rev-parse', 'HEAD').strip()
    return (urlish, git.relpath, branch, commit)


def get_remote_urlish(git, remotename):
    for line in git('remote', '-v').splitlines():
        [name, urlish, kind] = line.split()
        if kind == '(fetch)':
            if remotename is None and urlish.find('github.com') != -1:
                return urlish
            elif name == remotename:
                return urlish
        else:
            assert kind == '(push)', 'unknown remote kind: {}'.format(kind)

    assert False, 'remote {} not found.'.format(remotename)


def patch_git_urlish(urlish):
    PREFIX = 'git@github.com:'
    if urlish.startswith(PREFIX):
        guts = urlish[len(PREFIX):]
        return 'https://github.com/' + guts
    else:
        return urlish


class GitCmd (object):
    def __init__(self, path):
        relparts = []

        def pop_path(d):
            relparts.append(os.path.basename(d))
            return os.path.dirname(d)

        d = pop_path(path)
        while not os.path.isdir(os.path.join(d, '.git')):
            d = pop_path(d)

        self.repodir = d
        self.relpath = '/'.join(reversed(relparts))

    def __call__(self, *args):
        return subprocess.check_output(['git'] + list(args), cwd=self.repodir)


def calculate_urls(urlish, relpath, branch, commit):
    url = patch_git_urlish(urlish)
    urlp = urlparse.urlparse(url)
    urltmpl = '{scheme}://{netloc}/{basepath}/blob/{{}}/{relpath}'.format(
        scheme=urlp.scheme,
        netloc=urlp.netloc,
        basepath=urlp.path,
        relpath=relpath,
        )

    return (urltmpl.format(branch), urltmpl.format(commit))


def display_bare(f, mode, _relpath, _branch, branchurl, _commit, commiturl):
    if mode == 'branch' or mode == 'both':
        f.write('{}\n'.format(branchurl))
    if mode == 'commit' or mode == 'both':
        f.write('{}\n'.format(commiturl))


def display_comment(f, mode, relpath, branch, branchurl, commit, commiturl):
    commit = commit[:8]
    if mode == 'both':
        f.write(
            ('[``{relpath}`` at ``{commit}``]({commiturl}) '
             + '([latest on branch ``{branch}``]({branchurl}))\n')
            .format(
                relpath=relpath,
                commit=commit,
                commiturl=commiturl,
                branch=branch,
                branchurl=branchurl,
            ))
    elif mode == 'commit':
        f.write(
            '[``{relpath}`` at ``{commit}``]({url})\n'
            .format(
                relpath=relpath,
                commit=commit,
                url=commiturl,
            ))
    elif mode == 'branch':
        f.write(
            '[``{relpath}`` on branch ``{branch}``]({url})\n'
            .format(
                relpath=relpath,
                branch=branch,
                url=branchurl,
            ))
    else:
        assert False, 'unreachable code'


if __name__ == '__main__':
    main()
