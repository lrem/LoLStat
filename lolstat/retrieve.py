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
import lolstat.db

REQUEST_SLEEP = 1  # Don't spam requests too often
UNAUTH_SLEEP = 5 * 60  # Wait longer if rate limit hit

BASE_URL = 'https://prod.api.pvp.net/api/lol/%(region)s/'
RECENT = BASE_URL + 'v1.3/game/by-summoner/%(summonerId)s/recent'
RUNES = BASE_URL + 'v1.3/summoner/%(summonerIds)s/runes'
LEAGUE_ENTRY = BASE_URL + 'v2.3/league/by-summoner/%(summonerId)s/entry'
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
    res = requests.get(RECENT % {'region': region,
                                 'summonerId': summoner} + KEY)
    if res.status_code == 401:
        time.sleep(UNAUTH_SLEEP)
        return get_recent(region, summoner)
    return res.json()


def get_batch(region, summoners):
    """
    Retrieve recent games of `summoners`
    and everyone they played with recently.
    """
    ret = {summoner: get_recent(region, summoner) for summoner in summoners}
    for summoner in summoners:
        for game in ret[summoner]['games']:
            if not lolstat.db.game_in_db(game['gameId']):
                for fellow in game['fellowPlayers']:
                    fellowID = fellow['summonerId']
                    if fellowID not in ret:
                        ret[fellowID] = get_recent(region, fellowID)
    return ret


TIER_TO_INT = {'BRONZE': 0,
               'SILVER': 1,
               'GOLD': 2,
               'PLATINUM': 3,
               'DIAMOND': 4,
               'CHALLENGER': 5,
               }
DIVISION_TO_INT = {'V': 5,
                   'IV': 4,
                   'III': 3,
                   'II': 2,
                   'I': 1,
                   }


def get_ranks(region, summoners):
    """
    Retrieve league standings of `summoners`.
    """
    ret = []
    for summoner in summoners:
        entries = _get_ranks_single(region, summoner)
        for ent in entries:
            if(ent['queueType'] == 'RANKED_SOLO_5x5'):
                ent['tier'] = TIER_TO_INT[ent['tier']]
                ent['division'] = DIVISION_TO_INT[ent['rank']]  # O_o
                ret.append(ent)
    return ret


def _get_ranks_single(region, summoner):
    """
    Retrieve league standings of `summoner`.
    """
    time.sleep(REQUEST_SLEEP)
    res = requests.get(LEAGUE_ENTRY % {'region': region,
                                       'summonerId': summoner} + KEY)
    if res.status_code == 401:
        time.sleep(UNAUTH_SLEEP)
        return get_recent(region, summoner)
    if res.status_code == 404:  # A normals-only player
        return []
    return res.json()


def fill_missing_summoners(region):
    """
    Retrieve information of missing summoners:
        - summoner names
        - leagues
    """
    ids = lolstat.db.get_missing_summoners()
    raise NotImplementedError


def set_key(key=None):
    """
    Set the API key to the given one.
    If none is given, try to read one from `api.key` in current directory.
    """
    global KEY
    if key is None:
        key = open('api.key').readline().strip()
    KEY = '?api_key=' + key


if __name__ == '__main__':
    set_key()
    NAME = open('name').readline().strip()
    player = get_id('euw', NAME)
    batch = get_batch('euw', [player])
