# vim: fileencoding=utf-8

from dateutil import parser as date_parser
from lxml import objectify

import os
import requests
import urllib


class Screening:
    def __init__(self, item, lxml_event):
        assert isinstance(lxml_event, objectify.ObjectifiedElement)

        self.movie = item
        self.date = date_parser.parse(str(lxml_event.eventDate))
        self.venue = lxml_event.eventVenue
        self.buy_link = lxml_event.eventBuyLink

    def __str__(self):
        sane_date = self.date.strftime('%Y-%m-%d %H:%M')
        return '{} @ {}'.format(sane_date, self.venue)


class Item:
    def __init__(self, lxml_item):
        assert isinstance(lxml_item, objectify.ObjectifiedElement)

        self.postid = int(lxml_item.postid)
        self.title = str(lxml_item.title)
        self.link = str(lxml_item.link)
        # "To be announced" does not have a duration
        try:
            self.duration = date_parser.datetime.timedelta(minutes=int(lxml_item.eventDuration))
        except AttributeError:
            self.duration = None
        self.pub_date = date_parser.parse(str(lxml_item.pubDate))

        self.events = lxml_item.events

    def __repr__(self):
        return self.title

    def __str__(self):
        return self.title

    @property
    def slug(self):
        path = urllib.parse.urlparse(self.link).path

        # Both the leading url and the trailing /
        stripped_path = path.replace('/elokuvat/', '')
        if stripped_path.endswith('/'):
            stripped_path = stripped_path[:-1]

        return stripped_path

    @property
    def screenings(self):
        events = self.events.iter(tag='event')
        return tuple(Screening(self, evt) for evt in events)


class Feed:
    def __init__(self, feed_url, fname=None):
        """feed_url and optional cache fname
        """

        self.feed_url = feed_url
        self.fname = fname

        self._feed = None

        self._set_feed()

    def __str__(self):
        return 'Feed for {}'.format(self.feed_url)

    def _get_content(self):
        res = requests.get(self.feed_url)
        if res.status_code != 200:
            raise RuntimeError('Code {} getting feed'.format(res.status_code))

        return res.content

    def _cache_content(self, feed):
        with open(self.fname, 'wb') as f:
            f.write(feed)

    def _set_feed(self):
        if os.path.exists(self.fname) and os.stat(self.fname).st_size != 0:
            with open(self.fname, 'rb') as f:
                feed_content = f.read()
        else:
            feed_content = self._get_content()
            self._cache_content(feed_content)

        self._feed = feed_content

    @property
    def movies(self):
        assert self._feed is not None, 'self._feed is None'

        rss = objectify.fromstring(self._feed)

        items = rss.channel.iter('item')

        return tuple(Item(i) for i in items)

