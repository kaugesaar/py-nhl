from pprint import pprint
from bs4 import BeautifulSoup

import logging
import re
import urllib.request, urllib.error, urllib.parse
import urllib.parse
import sqlalchemy
import configparser
import datetime
import time
import sys
import getopt
import os

# Usage information
def usage():
    logmessage("usage information available on github wiki @ https://github.com/wellsoliver/py-nhl/wiki", loglevel=logging.CRITICAL)


def logmessage(message, **kwargs):
    loglevel = kwargs['loglevel'] if 'loglevel' in kwargs else logging.INFO

    logging.log(loglevel, message)

    if loglevel == logging.CRITICAL:
        raise SystemExit
    

# Replaces times w/ numeric times, etc
def fixvalues(row):
    values = []

    for value in row:
        if isinstance(value, str):
            if value.strip() in ['', '-']:
                value = None
            elif ':' in value: # time
                valuelist = [int(x) for x in value.split(':')]
                value = round(valuelist[0] + (valuelist[1] / 60.0), 2)
        values.append(value)

    return values


# Grabs a URL and returns a BeautifulSoup object
def fetchsoup(url, **kwargs):
    try:
        if 'verbose' in kwargs or True: logmessage('fetching %s' % url)
        res = urllib.request.urlopen(url)
        return BeautifulSoup(res.read())

    except urllib.error.HTTPError as e:
        logmessage('error code %s on %s' % (e.code, url), loglevel=logging.ERROR)
        return None
    except urllib.error.URLError as e:
        logmessage('bailing on %s (timeout of %s exceeded)' % (url, timeout), loglevel=logging.ERROR)
        return None


def processbox(game_id, conn):
    url = 'http://www.nhl.com/gamecenter/boxscore?id=%s' % game_id
    soup = fetchsoup(url)
    tables = soup.select('div.tableHeader')
    
    if len(tables) != 4:
        logmessage('no boxscore found for %s' % game_id, loglevel=logging.ERROR)
        return False

    for header in tables:
        table = header.find_next('table')
        playertype = 'skaters' if header.text.find('skaters') >= 0 else 'goalies'
        team = header.text.replace('skaters', '').replace('goaltenders', '').strip().upper()

        for row in table.select('tr.statsValues'):
            cells = row('td')
            values = [cell.text for cell in cells]
            player_id = re.search('=(\d+)$', cells[1].find('a')['href']).groups()[0]
            
            if playertype == 'goalies':
                if len(values) != 9: continue
                values = [value.replace(' ', '') for value in values]

                # [-2:] because a goalie had '-1-1' for saves
                params = [game_id, player_id, team] + \
                    values[2].split('-')[-2:] + \
                    values[3].split('-')[-2:] + \
                    values[4].split('-')[-2:] + \
                    values[5].split('-')[-2:] + \
                    values[6:9]

                if values[8] == '0:00':
                    # skip goalies with no TOI
                    continue

                query = 'DELETE FROM nhl.gamelogs_goalies WHERE player_id = %s AND game_id = %s'
                conn.execute(query, [player_id, game_id])
            
                query = 'INSERT INTO nhl.gamelogs_goalies VALUES(%s)' % (','.join(['%s'] * len(params)))
                conn.execute(query, fixvalues(params))
            
            if playertype == 'skaters':
                params = [game_id, player_id, team] + values[2:]
                if params[14].find('%') >= 0:
                    params[14] = int(params[14].replace('%', '')) / 100.0 # FO %

                query = 'DELETE FROM nhl.gamelogs_skaters WHERE player_id = %s AND game_id = %s'
                conn.execute(query, [player_id, game_id])
            
                query = 'INSERT INTO nhl.gamelogs_skaters VALUES(%s)' % (','.join(['%s'] * len(params)))
                conn.execute(query, fixvalues(params))


def processschedule(season, conn):
    # roster http://www.nhl.com/scores/htmlreports/20112012/RO021230.HTM
    # summary http://www.nhl.com/scores/htmlreports/20112012/GS021230.HTM
    # events http://www.nhl.com/scores/htmlreports/20112012/ES021230.HTM
    # faceoffs http://www.nhl.com/scores/htmlreports/20112012/FC021230.HTM
    # play by play http://www.nhl.com/scores/htmlreports/20112012/PL021230.HTM
    # shots http://www.nhl.com/scores/htmlreports/20112012/SS021230.HTM
    # home TOI http://www.nhl.com/scores/htmlreports/20112012/TH021230.HTM
    # away TOI http://www.nhl.com/scores/htmlreports/20112012/TV021230.HTM
    # box http://www.nhl.com/gamecenter/boxscore?id=2013010054
    
    url = 'http://www.nhl.com/ice/gamestats.htm?season=%s&gameType=2&team=&viewName=summary&pg=1' % season
    soup = fetchsoup(url)

    try:
        div = soup.find('div', 'pages')
        maxpage = int(urllib.parse.parse_qs(div.findAll('a')[-1]['href'])['pg'][0])
    except:
        maxpage = 1
    
    for page in range(1, maxpage + 1):
        url = 'http://www.nhl.com/ice/gamestats.htm?season=%s&gameType=2&team=&viewName=summary&pg=%s' % (season, page)
        soup = fetchsoup(url)

        table = soup.find('table', class_='stats')
        for row in table.find('tbody').findAll('tr'):
            values = [cell for cell in row.findAll('td')]
        
            try:
                anchor = values[0].find('a')
                game_id = '%s%s' % (str(season)[:4], re.search('GS(\d+)\.HTM$', anchor['href']).groups()[0])
                date = datetime.datetime.strptime(re.sub(r'\W+','', anchor.text), '%b%d%y').date()
                visitor = values[1].text
                visitor_score = values[2].text
                home = values[3].text
                home_score = values[4].text
                overtime = values[5].text == 'OT'
                shootout = values[5].text == 'SO'
                attendance = re.sub(r'\W+', '', values[-1].text)
            except:
                logmessage('cannot get game ID for schedule row', loglevel=logging.ERROR)
            
            if values[6].text == '':
                # no wining goalie - game in progress
                continue
        
            roster_url = 'http://www.nhl.com/scores/htmlreports/%s/RO%s.HTM' % (season, game_id)

            query = 'DELETE FROM nhl.gamelogs_skaters WHERE game_id = %s'
            conn.execute(query, [game_id])

            query = 'DELETE FROM nhl.gamelogs_goalies WHERE game_id = %s'
            conn.execute(query, [game_id])

            query = 'DELETE FROM nhl.games WHERE season = %s AND game_id = %s'
            conn.execute(query, [season, game_id])
            
            params = [game_id, season, date, visitor, home, visitor_score, home_score, overtime, shootout, attendance]
            query = 'INSERT INTO nhl.games VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            conn.execute(query, params)
            
            processbox(game_id, conn)


def processview(soup, position, view, tablename, season, conn):
    table     = soup.find('table', 'data')
    tablerows = table.find('tbody').findAll('tr')
    view      = view.lower();
    
    for row in tablerows:
        cellvalues = row.findAll('td')
        try:
            player_id = re.search('=(\d+)$', cellvalues[1].find('a')['href']).groups()[0]
        except:
            logmessage('cannot get player ID from row', loglevel=logging.ERROR)
            continue
        
        # Get the list of values we want based on the view
        values = [cell.text for cell in cellvalues]

        if view == 'summary' and position == 'S':
            values = [cell.text.replace(',', '') for cell in cellvalues[4:]]
        elif view == 'summary' and position == 'G':
            values = [cell.text.replace(',', '') for cell in cellvalues[3:]]
        elif view == 'timeonice':
            values = [cell.text.replace(',', '') for cell in cellvalues[4:]]
        elif view == 'faceoffpercentageall':
            values = [cell.text.replace(',', '') for cell in cellvalues[4:]]
            values.pop(9)
            values.pop(11)
            values.pop()
        elif view == 'points':
            values = values[4:]
        elif view == 'specialteamsaves':
            values = values[3:]
        elif view in ['bios', 'goaliebios']:
            values = values[:-11]
            # sometimes NHL.com lists a player on two pages... *shrug*
            query = 'SELECT * FROM players WHERE player_id = %s'
            result = conn.execute(query, [player_id])
            if result.rowcount > 0: continue
        if view in ['summary', 'timeonice', 'faceoffpercentageall', 'points', 'specialteamsaves']:
            # sometimes NHL.com lists a player on two pages... *shrug*
            query = 'DELETE FROM %s WHERE player_id = %s AND season = %s' % (tablename, player_id, season)
            conn.execute(query)

        # Custom handling
        if view in ['bios', 'goaliebios']:
            # Create a datetime object for DOB
            idx = 4 if view == 'bios' else 3
            try:
                dobstruct = time.strptime(values[idx], '%b %d \'%y')
                values[idx] = datetime.datetime.fromtimestamp(time.mktime(dobstruct))
            except:
                values[idx] = None
            
            # Set a position for a goalie
            if view == 'goaliebios':
                values.insert(3, 'G')

            values.pop(2) # Team
        elif view == 'summary' and position == 'S' and season < 20052006:
            # Game-tying goals removed for 2004/2005, removing it for prior years
            del values[11]

        # Insert season
        if view in ['summary', 'timeonice', 'faceoffpercentageall', 'points', 'specialteamsaves']:
            values.insert(0, season)

        # Insert player ID
        values.insert(0, player_id)
        
        query = 'INSERT INTO %s VALUES(%s)' % (tablename, ','.join(['%s'] * len(values)))
        conn.execute(query, fixvalues(values))


def main():
    pwd = os.path.dirname(__file__)
    if pwd == '': pwd = '.'
    config = configparser.ConfigParser()
    config.readfp(open('%s/py-nhl.ini' % pwd))

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M %p')

    SEASON = False
    VIEWS  = {
        'S': {
            'bios'                : 'players',
            'points'              : 'stats_skaters_points',
            'faceOffPercentageAll': 'stats_skaters_faceoff',
            'summary'             : 'stats_skaters_summary',
            'timeOnIce'           : 'stats_skaters_timeonice'
        }, 'G': {
            'goalieBios'      : 'players',
            'specialTeamSaves': 'stats_goalies_special',
            'summary'         : 'stats_goalies_summary'
        }
    }
    
    opts, args = getopt.getopt(sys.argv[1:], "s:", ["season="])

    for o, a in opts:
        if o in ('-s', '--season'): SEASON = int(a)

    if SEASON is False:
        logmessage('Season not passed', loglevel=logging.CRITICAL)

    try:
        ENGINE = config.get('database', 'engine')
        HOST = config.get('database', 'host')
        DATABASE = config.get('database', 'database')

        USER = None if not config.has_option('database', 'user') else config.get('database', 'user')
        SCHEMA = None if not config.has_option('database', 'schema') else config.get('database', 'schema')
        PASSWORD = None if not config.has_option('database', 'password') else config.get('database', 'password')
    except ConfigParser.NoOptionError:
        logmessage('Need to define engine, user, password, host, and database parameters', loglevel=logging.CRITICAL)

    if USER and PASSWORD: string = '%s://%s:%s@%s/%s' % (ENGINE, USER, PASSWORD, HOST, DATABASE)
    else:  string = '%s://%s/%s' % (ENGINE, HOST, DATABASE)

    try:
        db = sqlalchemy.create_engine(string)
        conn = db.connect()
        
        if SCHEMA: conn.execute('SET search_path TO %s' % SCHEMA)
    except:
        logmessage('Cannot connect to database', loglevel=logging.CRITICAL)

    for position, views in VIEWS.items():
        for view in sorted(views.keys()):
            table = views[view]
            if view not in ['bios', 'goalieBios']:
                conn.execute("DELETE FROM %s WHERE season = %s" % (table, SEASON))

            url = 'http://www.nhl.com/ice/playerstats.htm?season=%s&position=%s&gameType=2&viewName=%s&pg=1' % (SEASON, position, view)
            soup = fetchsoup(url)
            if not soup: continue

            # Get the max # of pages

            try:
                div = soup.find('div', 'pages')
                maxpage = int(urllib.parse.parse_qs(div.findAll('a')[-1]['href'])['pg'][0])
            except:
                maxpage = 1

            for page in range(1, maxpage + 1):
                url = 'http://www.nhl.com/ice/playerstats.htm?season=%s&position=%s&gameType=2&viewName=%s&pg=%s' % (SEASON, position, view, page)
                soup = fetchsoup(url)
                if not soup:
                    logmessage('cannot fetch url %s' % url, loglevel=logging.ERROR)
                    continue
                processview(soup, position, view, table, SEASON, conn)

    processschedule(SEASON, conn)

    conn.execute('UPDATE logging.last_update SET update = NOW()');
    conn.close()


if __name__ == '__main__':
    main()
