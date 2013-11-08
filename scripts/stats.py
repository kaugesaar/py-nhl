from pprint import pprint
from bs4 import BeautifulSoup, Tag

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

    if loglevel in [logging.CRITICAL, logging.ERROR]:
        logger = logging.getLogger("stderr")
        logger.log(loglevel, message)
    else:
        logger = logging.getLogger("stdout")
        logger.log(loglevel, message)

    if loglevel == logging.CRITICAL:
        raise SystemExit


def flip_name(name):
    inf = [s.strip() for s in name.split(',')]
    return '%s %s' % (inf[1], inf[0])


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


# Returns a player ID for a player name
def get_player_id(player_name, conn):
    query = 'SELECT DISTINCT player_id FROM players p LEFT JOIN players_names n USING (player_id) WHERE UPPER(p.player_name) = %s OR UPPER(n.player_name) = %s'
    row = conn.execute(query, [player_name, player_name]).fetchone()
    if not row:
        logmessage('Cannot get player_id from player name %s' % player_name, loglevel=logging.ERROR)
        return None
    return row['player_id']


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


# Processes box scores
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

                query = 'DELETE FROM gamelogs_goalies WHERE player_id = %s AND game_id = %s'
                conn.execute(query, [player_id, game_id])
            
                query = 'INSERT INTO gamelogs_goalies VALUES(%s)' % (','.join(['%s'] * len(params)))
                conn.execute(query, fixvalues(params))
            
            if playertype == 'skaters':
                params = [game_id, player_id, team] + values[2:]
                if params[14].find('%') >= 0:
                    params[14] = int(params[14].replace('%', '')) / 100.0 # FO %

                query = 'DELETE FROM gamelogs_skaters WHERE player_id = %s AND game_id = %s'
                conn.execute(query, [player_id, game_id])
            
                query = 'INSERT INTO gamelogs_skaters VALUES(%s)' % (','.join(['%s'] * len(params)))
                conn.execute(query, fixvalues(params))

# Processes rosters
def processroster(season, game_id, conn):
    real_game_id = str(game_id)[4:]
    url  = 'http://www.nhl.com/scores/htmlreports/%s/RO%s.HTM' % (season, real_game_id)
    soup = fetchsoup(url)
    game = {}
    rosters = {}
    tables = {}

    try:
        maintable   = soup.find_all('table', class_='tablewidth')[1]
        teamtable   = maintable.find_all('tr', recursive=False)[2].find('table')
        rostertable = maintable.find_all('tr', recursive=False)[3].find('table')

        game['visitor'] = teamtable('td')[0].text
        game['home']    = teamtable('td')[1].text
    
        tables['visitor_dressed'] = rostertable.find('tr').find_all('td', recursive=False)[0].find('table')
        tables['home_dressed']    = rostertable.find('tr').find_all('td', recursive=False)[1].find('table')

        tables['visitor_scratched'] = rostertable.find_all('tr', recursive=False)[3].find_all('table')[0]
        tables['home_scratched']    = rostertable.find_all('tr', recursive=False)[3].find_all('table')[1]
    except:
        logmessage('Cannot parse roster report from %s' % url, loglevel=logging.ERROR)
        return None

    for key in ['visitor', 'home']:
        rosters[key] = {'dressed': [], 'scratched': []}

        for status in rosters[key].keys():
            table = tables['%s_%s' % (key, status)]
            for row in table.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) == 2:
                    # Team
                    visitor = cells[0].text
                    home = cells[1].text
                if len(cells) == 3:
                    # Player
                    jersey, pos, player_name = [cell.text for cell in cells]
                    if player_name == 'Name' or not jersey.isdigit(): continue
                    player_id = get_player_id(player_name.replace('(C)', '').replace('(A)', '').strip(), conn)
                    rosters[key][status].append({'player_id': player_id, 'player_name': player_name})
    
    query = 'DELETE FROM games_rosters WHERE game_id = %s'
    conn.execute(query, [game_id])
    
    for team, roster in rosters.items():
        for status, players in roster.items():
            for player in players:
                if player['player_id'] is None: continue
                query = 'INSERT INTO games_rosters (game_id, team, status, player_id) VALUES(%s, %s, %s, %s)'
                params = [game_id, game[team], status, player['player_id']]
                conn.execute(query, params)


# Processes faceoff logs
def processfaceoff(season, game_id, conn):
    # A big old bunch of HTML parsing ahead, blegh
    real_game_id = str(game_id)[4:]
    url = 'http://www.nhl.com/scores/htmlreports/%s/FC%s.HTM' % (season, real_game_id)
    soup = fetchsoup(url)
    faceoffs = {}
    
    # TODO some better exception handling
    
    rows = soup.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if len(cells) == 7:
            # A new player
            player_name = cells[2].text
            if player_name.find('Player') >= 0: continue
            inf = [s.strip() for s in player_name.split(',')]
            player_id = get_player_id('%s %s' % (inf[1], inf[0]), conn)
            
            if player_id:
                if player_id not in faceoffs: faceoffs[player_id] = {}
            else:
                continue
            
        elif len(cells) == 8:
            # A stat row
            vs, o, d, n, t = [c.text.strip() for c in cells[3:8]]
            vs = re.sub('\d+', '', vs.replace('vs.', '').replace(' C ', '').replace(' L ', '').replace(' R ', '').replace(' D ', '').strip())
            inf = [s.strip() for s in vs.split(',')]
            opp = get_player_id('%s %s' % (inf[1], inf[0]), conn)

            if player_id is None or opp is None: continue
            
            faceoffs[player_id][opp] = {
                'offensive': o.split('/')[0].strip().split('-'),
                'defensive': d.split('/')[0].strip().split('-'),
                'neutral': n.split('/')[0].strip().split('-'),
                'total': t.split('/')[0].strip().split('-')
            }
    
    if (len(faceoffs.keys())) == 0:
        logmessage('Cannot parse faceoff report from %s' % url, loglevel=logging.ERROR)
        return None
    
    query = 'DELETE FROM games_faceoffs WHERE game_id = %s'
    conn.execute(query, [game_id])
    for player_id, records in faceoffs.items():
        for opponent_id, draws in records.items():
            for zone, totals in draws.items():
                if len(totals) == 1:
                    wins = 0
                    attempts = 0
                else:
                    wins, attempts = totals
                query = 'INSERT INTO games_faceoffs (game_id, player_id, versus, zone, wins, attempts) VALUES(%s, %s, %s, %s, %s, %s)'
                params = [game_id, player_id, opponent_id, zone, wins, attempts]
                conn.execute(query, params)


# Time on ice
def processtoi(season, game_id, conn):
    real_game_id = str(game_id)[4:]
    toi = {}
    
    for key in ['home', 'visitor']:
        toi[key] = {}
        url_key = 'H' if key == 'home' else 'V'
        url = 'http://www.nhl.com/scores/htmlreports/%s/T%s%s.HTM' % (season, url_key, real_game_id)
        soup = fetchsoup(url)
        
        if soup is None:
            logmessage('Cannot fetch %s TOI report: %s' % (key, url))
            return None
        
        for cell in soup('td', class_='playerHeading'):
            player_name = flip_name(re.sub('\d+', '', cell.text))
            player_id = get_player_id(player_name, conn)
            toi[key][player_id] = []

            parent = cell.parent
            for row in parent.next_siblings:
                if isinstance(row, Tag):
                    cells = row.find_all('td', recursive=False)
                    if len(cells) == 1:
                        break
                    elif cells[0].text.find('Shift #') == -1 and len(cells) == 6:
                        shift = {
                            'shift'         : cells[0].text,
                            'period'        : 4 if cells[1].text == 'OT' else cells[1].text,
                            'start_elapsed' : cells[2].text.split('/')[0].strip(),
                            'start_game'    : cells[2].text.split('/')[1].strip(),
                            'end_elapsed'   : cells[3].text.split('/')[0].strip(),
                            'end_game'      : cells[3].text.split('/')[1].strip(),
                            'duration'      : cells[4].text,
                            'event'         : None if len(cells[5].text.strip()) == 0 else cells[5].text.strip()
                        }
                        toi[key][player_id].append(shift)

    if len(toi['home'].keys()) == 0 or len(toi['visitor'].keys()) == 0:
            logmessage('Cannot parse %s TOI report: %s' % (key, url))
            return None

    query = 'DELETE FROM games_toi WHERE game_id = %s'
    conn.execute(query, [game_id])
    for key, players in toi.items():
        for player_id, shifts in players.items():
            for shift in shifts:
                params = [game_id, player_id, shift['period'], shift['shift'], shift['start_elapsed'], shift['start_game'], shift['end_elapsed'], shift['end_game'], shift['duration'], shift['event']]
                query = 'INSERT INTO games_toi (game_id, player_id, period, shift, start_elapsed, start_game, end_elapsed, end_game, duration, event) VALUES(%s)' % ','.join(['%s'] * len(params))
                conn.execute(query, fixvalues(params))


def processschedule(season, do_full, conn):
    # summary http://www.nhl.com/scores/htmlreports/20112012/GS021230.HTM
    # events http://www.nhl.com/scores/htmlreports/20112012/ES021230.HTM
    # play by play http://www.nhl.com/scores/htmlreports/20112012/PL021230.HTM
    # shots http://www.nhl.com/scores/htmlreports/20112012/SS021230.HTM
    # home TOI http://www.nhl.com/scores/htmlreports/20112012/TH021230.HTM
    # away TOI http://www.nhl.com/scores/htmlreports/20112012/TV021230.HTM
    
    url = 'http://www.nhl.com/ice/gamestats.htm?season=%s&gameType=2&team=&viewName=summary&pg=1' % season
    soup = fetchsoup(url)

    try:
        div = soup.find('div', 'pages')
        maxpage = int(urllib.parse.parse_qs(div.find_all('a')[-1]['href'])['pg'][0])
    except:
        maxpage = 1
    
    for page in range(1, maxpage + 1):
        url = 'http://www.nhl.com/ice/gamestats.htm?season=%s&gameType=2&team=&viewName=summary&pg=%s' % (season, page)
        soup = fetchsoup(url)

        table = soup.find('table', class_='stats')
        for row in table.find('tbody').find_all('tr'):
            values = [cell for cell in row.find_all('td')]
        
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

            query = 'DELETE FROM gamelogs_skaters WHERE game_id = %s'
            conn.execute(query, [game_id])

            query = 'DELETE FROM gamelogs_goalies WHERE game_id = %s'
            conn.execute(query, [game_id])
            
            query = 'SELECT * FROM games WHERE season = %s AND game_id = %s'
            rows = conn.execute(query, [season, game_id]).fetchall()

            if len(rows) == 0:
                params = [game_id, season, date, visitor, home, visitor_score, home_score, overtime, shootout, attendance]
                query = 'INSERT INTO games VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                conn.execute(query, params)
            
            diff = datetime.datetime.today().date() - date

            # Only process games in last five days or all if set to full
            if do_full or diff.days <= 5:
                processbox(game_id, conn)
                processroster(season, game_id, conn)
                processfaceoff(season, game_id, conn)
                processtoi(season, game_id, conn)


def processview(soup, position, view, tablename, season, conn):
    table     = soup.find('table', 'data')
    tablerows = table.find('tbody').find_all('tr')
    view      = view.lower();
    
    for row in tablerows:
        cellvalues = row.find_all('td')
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
    
    DO_FULL = False
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
    
    opts, args = getopt.getopt(sys.argv[1:], "s:f", ["season=", "full"])

    for o, a in opts:
        if o in ('-s', '--season'): SEASON = int(a)
        elif o in ('-f', '--full'): DO_FULL = True

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
    except Exception as e:
        logmessage('Cannot connect to database: %s' % e, loglevel=logging.CRITICAL)

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
                maxpage = int(urllib.parse.parse_qs(div.find_all('a')[-1]['href'])['pg'][0])
            except:
                maxpage = 1

            for page in range(1, maxpage + 1):
                url = 'http://www.nhl.com/ice/playerstats.htm?season=%s&position=%s&gameType=2&viewName=%s&pg=%s' % (SEASON, position, view, page)
                soup = fetchsoup(url)
                if not soup:
                    logmessage('cannot fetch url %s' % url, loglevel=logging.ERROR)
                    continue
                processview(soup, position, view, table, SEASON, conn)

    processschedule(SEASON, DO_FULL, conn)


if __name__ == '__main__':
    main()
