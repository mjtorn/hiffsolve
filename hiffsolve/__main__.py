# vim: fileecoding=utf-8

from . import feed2016

import sys

TMPFILE = '/tmp/hiff2016.feed'
FEED_URL = 'http://hiff.fi/elokuvat/feed/'


def main():
    feed = feed2016.Feed(FEED_URL, fname=TMPFILE)

    for item in feed.movies:
        print(item.slug)
        for screening in item.screenings:
            print('\t{}'.format(screening))

    return 0

sys.exit(main())

