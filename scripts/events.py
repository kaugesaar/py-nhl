from pprint import pprint
from bs4 import BeautifulSoup

import re
import json
import urllib.request, urllib.error, urllib.parse
import sqlalchemy
import configparser
import datetime
import time
import sys
import getopt
import calendar
import os
import logging


def logmessage(message, **kwargs):
    loglevel = kwargs['loglevel'] if 'loglevel' in kwargs else logging.INFO

    if loglevel == logging.CRITICAL:
        logger = logging.getLogger("stderr")
        logger.log(loglevel, message)
        raise SystemExit
    else:
        logger = logging.getLogger("stdout")
        logger.log(loglevel, message)


# Usage information
def usage():
    logmessage("usage information available on github wiki @ https://github.com/wellsoliver/py-nhl/wiki", loglevel=logging.CRITICAL)


# Returns list of games
def getgamelist(**kwargs):
    months = []
    games = []
    dates = []

    if 'date' in kwargs:
        dates.append(kwargs['date'])
    elif 'year' in kwargs:
        year = kwargs['year']
        if 'month' in kwargs:
            months.append(kwargs['month'])
        else:
            for month in range(1,13):
                months.append(month)

        for month in months:
            url = 'http://www.nhl.com/ice/ajax/gamecalendarjson.htm?month=%d&year=%d' % (month, year)
            res = fetchurl(url)
            gamelist = json.loads(res)

            for date in gamelist['gameDates']:
                if date['n'] > 0:
                    gamedate = datetime.datetime.strptime(date['gd'], '%m/%d/%Y')
                    if 'day' in kwargs and gamedate.day != kwargs['day']: continue
                    dates.append(gamedate)

    for date in dates:
        gamelisturl = 'http://www.nhl.com/ice/ajax/GCScoreboardJS?today=%s' % date.strftime("%m/%d/%Y")
        try:
            gamelistraw = fetchurl(gamelisturl)
        
            if (len(gamelistraw) == 0): return []
        
            # HACK ALERT substring out the call to the javascript method loadScoreboard() to get raw JSON
            gamelistraw = gamelistraw[15:-1]
            gamelist = json.loads(gamelistraw)['games']
        except:
            gamelist = []

        for game in gamelist:
            game['date'] = date # Keep track of this
            games.append(game)

    return games


# Grabs a URL
def fetchurl(url):
    try:
        print(url)
        res = urllib.request.urlopen(url)
        return res.read()
    except:
        return None


# Gets a specific game
def getgame(game_id, season):
    gameurl = 'http://live.nhl.com/GameData/%s/%s/PlayByPlay.json' % (season, game_id)

    try:
        content = fetchurl(gameurl)
        obj = json.loads(content)
        return obj['data']['game']
    except:
        return None


# Processes an event
def processevent(game_id, event, conn):
    event_id = event['eventid']

    headers = [
        'event_id',
        'formal_event_id',
        'game_id',
        'period',
        'strength',
        'type',
        'shot_type',
        'description',
        'player_id',
        'team_id',
        'xcoord',
        'ycoord',
        'video_url',
        'altvideo_url',
        'home_score',
        'away_score',
        'home_sog',
        'away_sog',
        'time',
        'goalie_id'
    ]
    
    goalie_id = event['g_goalieID'] if 'g_goalieID' in event and event['g_goalieID'] != '' else None
    if goalie_id is None and 'pid2' in event and len(str(event['pid2'])) > 0:
        goalie_id = event['pid2']
    
    values = [
        event_id,
        event['formalEventId'],
        game_id,
        event['period'],
        event['strength'],
        event['type'],
        event['g_shotType'] if 'g_shotType' in event and event['g_shotType'] != '' else None,
        None if 'desc' not in event else event['desc'],
        event['pid'] if 'pid' in event else None,
        event['teamid'],
        event['xcoord'],
        event['ycoord'],
        event['video'] if 'video' in event else None,
        event['altVideo'] if 'altVideo' in event else None,
        event['hs'],
        event['as'],
        event['hsog'] if event['type'] in ['Goal', 'Shot'] else None,
        event['asog'] if event['type'] in ['Goal', 'Shot'] else None,
        event['time'],
        goalie_id
    ]
    
    sql = 'INSERT INTO events (%s) VALUES(%s)' % (','.join(headers), ','.join(['%s'] * len(values)))
    conn.execute(sql, values)

    if 'aoi' in event:
        for player_id in event['aoi']:
            sql = 'INSERT INTO events_players (game_id, event_id, which, player_id) VALUES(%s, %s, %s, %s)'
            conn.execute(sql, [game_id, event_id, 'away', player_id])

    if 'hoi' in event:
        for player_id in event['hoi']:
            sql = 'INSERT INTO events_players (game_id, event_id, which, player_id) VALUES(%s, %s, %s, %s)'
            conn.execute(sql, [game_id, event_id, 'home', player_id])

    if 'apb' in event:
        for player_id in event['apb']:
            sql = 'INSERT INTO events_penaltybox (game_id, event_id, which, player_id) VALUES(%s, %s, %s, %s)'
            conn.execute(sql, [game_id, event_id, 'away', player_id])

    if 'hpb' in event:
        for player_id in event['hpb']:
            sql = 'INSERT INTO events_penaltybox (game_id, event_id, which, player_id) VALUES(%s, %s, %s, %s)'
            conn.execute(sql, [game_id, event_id, 'home', player_id])


# Processes a game
def processgame(season, game, conn):
    
    game_id = game['id']
    fetchedgame = getgame(game_id, season)

    if fetchedgame is None:
        return None

    # Clear out data
    query = 'DELETE FROM events_players WHERE game_id = %s'
    conn.execute(query, [game_id])

    query = 'DELETE FROM events_penaltybox WHERE game_id = %s'
    conn.execute(query, [game_id])

    query = 'DELETE FROM events WHERE game_id = %s'
    conn.execute(query, [game_id])

    values = [season, \
        game_id, \
        fetchedgame['awayteamid'], \
        fetchedgame['hometeamid'], \
        game['date'], \
        game['hts'], \
        game['ats'], \
        game['rl'], \
        game['gcl'], \
        game['gcll'], \
        game['bs'], \
        game['bsc'], \
        game['gs']
    ]

    for event in fetchedgame['plays']['play']:
        processevent(game_id, event, conn)


def main():
    pwd = os.path.dirname(__file__)
    if pwd == '': pwd = '.'
    config = configparser.ConfigParser()
    config.readfp(open('%s/py-nhl.ini' % pwd))

    formatter = logging.Formatter('%(levelname)s | %(asctime)s | %(message)s', datefmt='%m/%d/%Y %I:%M %p')

    s1 = logging.StreamHandler(stream=sys.stdout)
    s1.setLevel(logging.DEBUG)
    s1.setFormatter(formatter)

    s2 = logging.StreamHandler(stream=sys.stderr)
    s2.setLevel(logging.DEBUG)
    s2.setFormatter(formatter)

    stdout = logging.getLogger("stdout")
    stderr = logging.getLogger("stderr")
    stdout.addHandler(s1)
    stderr.addHandler(s2)

    stdout.setLevel(logging.DEBUG)
    stderr.setLevel(logging.DEBUG)

    try:
        ENGINE = config.get('database', 'engine')
        HOST = config.get('database', 'host')
        DATABASE = config.get('database', 'database')

        USER = None if not config.has_option('database', 'user') else config.get('database', 'user')
        SCHEMA = None if not config.has_option('database', 'schema') else config.get('database', 'schema')
        PASSWORD = None if not config.has_option('database', 'password') else config.get('database', 'password')

    except configparser.NoOptionError:
        print('Need to define engine, user, password, host, and database parameters')
        raise SystemExit

    if USER and PASSWORD: string = '%s://%s:%s@%s/%s' % (ENGINE, USER, PASSWORD, HOST, DATABASE)
    else:  string = '%s://%s/%s' % (ENGINE, HOST, DATABASE)

    try:
        db = sqlalchemy.create_engine(string)
        conn = db.connect()
    except:
        print('Cannot connect to database')
        raise SystemExit

    if SCHEMA: conn.execute('SET search_path TO %s' % SCHEMA)
    
    SEASON = False
    YEAR = False
    MONTH = False
    DAY = False
    gameargs = {}

    try:
        opts, args = getopt.getopt(sys.argv[1:], "s:y:m:d:", ["season=", "year=", "month=", "day="])
    except getopt.GetoptError as e:
        usage()

    for o, a in opts:
        if o in ('-y', '--year'): YEAR = int(a)
        elif o in ('-m', '--month'): MONTH = int(a)
        elif o in ('-d', '--day'): DAY = int(a)
        elif o in ('-s', '--season'): SEASON = int(a)

    if SEASON is False: usage()
    
    if YEAR:
        gameargs['year'] = YEAR
        if MONTH:
            gameargs['month'] = MONTH
            if DAY:
                gameargs['day'] = DAY
    else:
        # Just yesterday!
        gameargs['date'] = datetime.datetime.today() - datetime.timedelta(1)

    gamelist = getgamelist(**gameargs)
    for game in gamelist:
        processgame(SEASON, game, conn)


if __name__ == '__main__':
    main()
