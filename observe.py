#!/usr/bin/env python3
"""
Add a summoner to the observed pool
===================================

A command line utility to add a summoner to the observed list.
"""

import argparse
import lolstat.retrieve
import lolstat.db

REGION = 'euw'  # No transatlantic, no EU 2, for now

parser = argparse.ArgumentParser()
parser.add_argument('name', type=str)
args = parser.parse_args()

lolstat.retrieve.set_key()

sid = lolstat.retrieve.get_id(REGION, args.name)
lolstat.db.add_summoner(args.name, sid)
