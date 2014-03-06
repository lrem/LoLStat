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

REGION = 'euw'  # No transatlantic, no EU 2, for now
INTERVAL = 10*60*60  # No need to check more often than a short game time
VERBOSE = True


def main():
    lolstat.retrieve.set_key()
    last_ranks = 0
    while True:
        if VERBOSE:
            print("Activating")
        start = time.time()
        ids = lolstat.db.get_observed_summoners()
        batch = lolstat.retrieve.get_batch(REGION, ids)
        lolstat.db.store_batch(batch)
        end = time.time()
        if VERBOSE:
            print("Batch in %f seconds" % (end - start, ))
        mid = time.time()
        ids = lolstat.db.get_stale_ranks()
        ranks = lolstat.retrieve.get_ranks(REGION, ids)
        lolstat.db.store_ranks(ranks)
        lolstat.db.update_last_ranks(ids)
        end = time.time()
        last_ranks = start
        if VERBOSE:
            print("Ranks in %f seconds" % (end - mid, ))
        time.sleep(INTERVAL - (end - start))

if __name__ == '__main__':
    main()
