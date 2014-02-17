#!/usr/bin/env python3
"""
Retrieval from LoL API
======================

This module allows batch retrieval of recent history records.
All `get_` functions return JSON parsed into dictionaries of dictionaries,
except the `get_id`.
"""

import requests
import time

REQUEST_SLEEP = 1  # Don't spam requests too often

BASE_URL = 'https://prod.api.pvp.net/api/lol/%(region)s/'
RECENT = BASE_URL + 'v1.3/game/by-summoner/%(summonerId)s/recent'
RUNES = BASE_URL + 'v1.3/summoner/%(summonerIds)s/runes'
MASTERIES = BASE_URL + 'v1.3/summoner/%(summonerIds)s/masteries'
NAME = BASE_URL + 'v1.3/summoner/%(summonerIds)s/name'
BY_NAME = BASE_URL + 'v1.3/summoner/by-name/%(summonerNames)s'
KEY = '?api_key='


def get_id(region, name):
    """
    Retrieve ID of a summoner given by `name`.
    """
    json = requests.get(BY_NAME % {'region': region,
                                   'summonerNames': name} + KEY).json()
    return list(json.values())[0]['id']


def get_recent(region, summoner):
    """
    Retrieve recent games of `summoner`.
    """
    time.sleep(REQUEST_SLEEP)
    return requests.get(RECENT % {'region': region,
                                  'summonerId': summoner} + KEY).json()


def get_surrounding(region, summoner):
    """
    Retrieve recent games of `summoner` and everyone he played with recently.
    """
    own = get_recent(region, summoner)
    surrounding = {summoner: own}
    for game in own['games']:
        for fellow in game['fellowPlayers']:
            fellowID = fellow['summonerId']
            if fellowID not in surrounding:
                surrounding[fellowID] = get_recent(region, fellowID)
    return surrounding


if __name__ == '__main__':
    KEY += open('api.key').readline().strip()
    NAME = open('name').readline().strip()
    player = get_id('euw', NAME)
    recent = get_recent('euw', player)
    surrounding = get_surrounding('euw', player)
    print(surrounding)
