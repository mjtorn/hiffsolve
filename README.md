# HIFF solver

Make booking tickets easier for the [Helsinki International Film Festival](http://hiff.fi/)

This was meant to give points to screenings and solve which screenings to go to, but
it started taking too much time so I settled with something that dumps a CSV. Too much
time being like two hours.

The CSV needs a bit of autosizing cells and deleting of empties, but in the end it's
quite a usable spreadsheet to eg. bold the screenings you want to go to and then buy
the tickets manually.

For test data:

    $ cp test_data/hiff2016.feed /tmp/

