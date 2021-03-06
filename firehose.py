#!/usr/bin/env python3
"""
Data retrieval daemon
=====================

A simple thing that will get the list of summoners to observe
and get all the data we want to get about them,
in an endless loop.
"""

import time
import lolstat.retrieve
import lolstat.db

INTERVAL = 10*60  # No need to check more often than a short game time
VERBOSE = True


def main():
    lolstat.retrieve.set_key()
    while True:
        if VERBOSE:
            print("Activating")
        try:
            start = time.time()
            ids = lolstat.db.get_observed_summoners()
            batch = lolstat.retrieve.get_batch(ids)
            lolstat.db.store_batch(batch)
            end = time.time()
            if VERBOSE:
                print("Batch in %f seconds" % (end - start, ))
            mid = time.time()
            ids = lolstat.db.get_stale_ranks()
            ranks = lolstat.retrieve.get_ranks(ids)
            lolstat.db.store_ranks(ranks)
            lolstat.db.update_last_ranks(ids)
            end = time.time()
            if VERBOSE:
                print("Ranks in %f seconds" % (end - mid, ))
            mid = time.time()
            lolstat.retrieve.fill_missing_summoners()
        except:
            print("FAILURE")
        end = time.time()
        if VERBOSE:
            print("Missing summoners in %f seconds" % (end - mid, ))
        time.sleep(max(0, INTERVAL - (end - start)))

if __name__ == '__main__':
    main()
