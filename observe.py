#!/usr/bin/env python3
"""
Add a summoner to the observed pool
===================================

A command line utility to add a summoner to the observed list.
"""

import argparse
import lolstat.retrieve
import lolstat.db

parser = argparse.ArgumentParser()
parser.add_argument('name', type=str)
args = parser.parse_args()

lolstat.retrieve.set_key()

sid = lolstat.retrieve.get_id(args.name)
lolstat.db.add_summoner(args.name, sid)
