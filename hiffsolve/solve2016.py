# vim: fileecoding=utf-8

from . import feed2016

import csv
import io
import itertools
import os


class Solver:
    def __init__(self, feed, movie_list):
        assert isinstance(feed, feed2016.Feed)
        if not os.path.exists(movie_list):
            raise RuntimeError('movie_list file not found {}'.format(movie_list))

        self.feed = feed
        self.movie_list = movie_list

        self.movies = self._parse_movie_list()

    def _parse_movie_list(self):
        d = {}
        for movie_line in open(self.movie_list, 'rb'):
            movie_name = movie_line.strip()
            if not movie_name:
                continue

            movie = self.feed.find(movie_name)
            d[movie.slug] = movie

        return d

    def _date_group_key(self, screening):
        return screening.date.strftime('%Y-%m-%d')

    def by_date(self):
        d = {}

        screenings = tuple(itertools.chain(*(m.screenings for m in self.movies.values())))
        screenings = sorted(screenings, key=lambda s: s.date)

        for date, screenings in itertools.groupby(screenings, key=self._date_group_key):
            screenings = tuple(sorted(screenings, key=lambda s: s.date))
            d.setdefault(date, []).extend(screenings)

        return d

    def get_csv(self):
        d = self.by_date()
        ds = []

        dates = sorted(d.keys())

        f = io.StringIO()
        w = csv.DictWriter(f, fieldnames=dates)

        w.writeheader()
        for date, screenings in sorted(d.items(), key=lambda kv: kv[0]):
            # print(date)
            for screening in screenings:
                time = screening.date.strftime('%H:%M')
                movie = screening.movie
                screening = '{} {}'.format(time, movie)
                ds.append({date: screening})
            # print(screenings)
        for d in ds:
            w.writerow(d)

        f.seek(0)
        return f.read()

