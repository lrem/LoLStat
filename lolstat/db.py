#!/usr/bin/env python3
"""
Database storage
================

This module performs all database operations.
"""

import sqlite3
from functools import wraps

DB_PATH = 'lolstat.db'
DBH = sqlite3.connect(DB_PATH)


def transaction(func):
    """
    A wrapper for top-level transactions, rollbacks transaction on exception.
    """
    @wraps(func)  # This preserves meta-data like docstrings
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
            DBH.commit()
        except:
            DBH.rollback()
            raise
    return wrapper


@transaction
def store_batch(data):
    """
    Store the data of recent matches of multiple summoners.
    This is retrieved as hash of lists of recent games for some summoners
    and for all summoners they played with recently.
    This gives us some data we did not intentionally ask for,
    but can be useful as data points for aggregate statistics.
    """
    for player in data:
        for game in data[player]['games']:
            if not game_in_db(game['gameId']):
                _store_game(game)
            if not _stats_in_db(game['gameId'], player):
                _store_stats(game, player)


def _stats_in_db(game, player):
    """
    Determine whether the stats are already in the database
    """
    cur = DBH.execute('select count(*) from stats'
                      ' where gameId=? and summonerId=?', [game, player])
    return bool(cur.fetchone()[0])


def _store_stats(game, player):
    """
    Store stats for a game by a single player.
    These consist of summoner spells stored in game object
    and the stats object within it.
    """
    keys = ['summonerId', 'gameId', 'spell1', 'spell2']
    values = [player, game['gameId'], game['spell1'], game['spell2']]
    for key, value in game['stats'].items():
        keys.append(key)
        values.append(value)
    keys_s = '(' + ','.join(keys) + ')'
    placeholders = '(' + ','.join(['?'] * len(keys)) + ')'
    DBH.execute('insert into stats ' + keys_s + ' values ' + placeholders,
                list(map(int, values)))  # They are all supposed to be INTEGER


def _store_game(game):
    """
    Put into the database the meta-data of the game.
    """
    DBH.execute('insert into game values(?, ?, ?, ?, ?, ?, ?)',
                [game['gameId'],
                 game['mapId'],
                 game['gameMode'],
                 game['gameType'],
                 game['subType'],
                 game['invalid'],
                 game['createDate'],
                 ])
    if 'fellowPlayers' not in game:
        return  # This apparently can happen, contradictory to API docs
    for pick in game['fellowPlayers']:
        DBH.execute('insert into pick values (?, ?, ?, ?)',
                    [game['gameId'],
                     pick['championId'],
                     pick['summonerId'],
                     pick['teamId'],
                     ])


def game_in_db(gameId):
    """
    Determine whether the game is already in the database
    """
    cur = DBH.execute('select count(*) from game where gameId=?', [gameId])
    return bool(cur.fetchone()[0])
