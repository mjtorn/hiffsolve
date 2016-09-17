# vim: fileecoding=utf-8

from . import feed2016, solve2016

import sys

TMPFILE = '/tmp/hiff2016.feed'
FEED_URL = 'http://hiff.fi/elokuvat/feed/'


def main(args):
    if len(args) != 1:
        print('Give path to file with one movie name per line')
        return 1

    feed = feed2016.Feed(FEED_URL, fname=TMPFILE)
    solver = solve2016.Solver(feed, args[0])

    print(solver.get_csv())

    return 0

sys.exit(main(sys.argv[1:]))

