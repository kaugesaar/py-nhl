from . import NHLObject, parse_time
from bs4 import BeautifulSoup, Tag
from datetime import datetime
from pprint import pprint


import urllib.request, urllib.error, urllib.parse
import logging
import re
import json


class PlayByPlay(NHLObject):
    def __init__(self, season, game_id):
        super(PlayByPlay, self).__init__()
        self.season = season
        self.game_id = game_id

        self.periods = {}
        
        url = 'scores/htmlreports/%s/PL%s.HTM' % (season, game_id)
        c = self.geturl(url)
        soup = BeautifulSoup(c)
        self.visitor = str(soup.select('table#Visitor')[0].find_all('td')[-1].contents[0])
        self.home = str(soup.select('table#Home')[0].find_all('td')[-1].contents[0])
        
        table = soup.find('table').find_all('tr', recursive=False)[2]
        teamcells = [cell.text.strip() for cell in table.find_all('td')[-2:]]
        teamcells = [cell.replace(' On Ice', '') for cell in teamcells]
        self.visitor_short, self.home_short = teamcells
        
        for row in soup.find_all('tr', class_='evenColor'):
            cells = row.find_all('td', recursive=False)
            eventno, period, strength = [c.text for c in cells[0:3]]
            if len(cells[3].text.strip()) == 0: # Only in the Peverley game :(
                elapsed = None
                game = None
            else:
                elapsed, game = [c.string for c in cells[3].contents]
            
            event_type, description = [c.text for c in cells[4:6]]
            ice = {self.visitor_short: [], self.home_short: []}

            for i, cell in enumerate(cells[6:8]):
                icetable = cell.find('table')
                if icetable is None: # GEND events don't have players
                    continue
                for playertable in icetable.find_all('table'):
                    pcells = [x.find('td') for x in playertable.find_all('tr')]
                    font = pcells[0].find('font')
                    pos = pcells[1].text.strip()
                    if not font or 'title' not in font.attrs.keys():
                        self.logmessage('No title attribute found for item')
                        continue
                    
                    player = re.sub('.+?- ', '', font['title'])
                    jersey = font.text
                    teamkey = self.visitor_short if i == 0 else self.home_short
                    longname = self.visitor if i == 0 else self.home
                    side = 'visitor' if i == 0 else 'home'
                    record = {
                        'player': player,
                        'jersey': jersey,
                        'pos': pos,
                        'team': teamkey,
                        'longname': longname,
                        'side': side
                    }
                    ice[teamkey].append(record)

            if period not in self.periods:
                self.periods[period] = []
            
            # Deal with crappy information
            if elapsed and elapsed.find('0-1') >= 0:
                continue

            self.periods[period].append({
                'season': season,
                'game_id': game_id,
                'eventno': eventno,
                'period': period,
                'strength': strength.strip(),
                'time_elapsed': parse_time(elapsed),
                'time_game': parse_time(game),
                'event_type': event_type,
                'description': description,
                'ice': ice,
                'period': period
            })


class Faceoffs(NHLObject):
    def __init__(self, season, game_id):
        super(Faceoffs, self).__init__()
        self.season = season
        self.game_id = game_id
        self.faceoffs = {}
        
        url = 'scores/htmlreports/%s/FC%s.HTM' % (season, game_id)
        c = self.geturl(url)
        soup = BeautifulSoup(c)
        
        for row in soup.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) == 7:
                # A new player
                name = ' '.join(reversed(cells[2].text.split(','))).strip()
                if name.find('Player') >= 0: continue
            
                if name not in self.faceoffs:
                    self.faceoffs[name] = {}
            
            elif len(cells) == 8:
                # A stat row
                vs, o, d, n, t = [c.text.strip() for c in cells[3:8]]
                vs = re.sub('\d+', '', vs)
                
                for stripkey in ['vs.', ' C ', ' L ', ' R ']:
                    vs = vs.replace(stripkey, '')
                
                opponent = ' '.join(reversed(vs.strip().split(','))).strip()
            
                # faceoffs: won/totals
                self.faceoffs[name][opponent] = {
                    'O': o.split('/')[0].strip().split('-'),
                    'D': d.split('/')[0].strip().split('-'),
                    'N': n.split('/')[0].strip().split('-'),
                    'T': t.split('/')[0].strip().split('-')
                }


class TimeOnIce(NHLObject):
    def __init__(self, season, game_id):
        super(TimeOnIce, self).__init__()
        self.season = season
        self.game_id = game_id
        self.toi = {}
        
        for key in ['H', 'V']:
            url = 'scores/htmlreports/%s/T%s%s.HTM' % (season, key, game_id)
            c = self.geturl(url)
            soup = BeautifulSoup(c)
            team = soup.select('td.teamHeading')[0].text

            self.toi[team] = {}

            for cell in soup.find_all('td', class_='playerHeading'):
                playername = ''.join(reversed(re.sub('\d+', '', cell.text).split(', ')))
                self.toi[team][playername] = []

                parent = cell.parent
                for row in parent.next_siblings:
                    if isinstance(row, Tag):
                        cells = row.find_all('td', recursive=False)
                        if len(cells) == 1:
                            break
                        elif cells[0].text.find('Shift #') == -1 and len(cells) == 6:
                            shift = {
                                'shift': cells[0].text,
                                'period': 4 if cells[1].text == 'OT' else cells[1].text,
                                'start_elapsed': cells[2].text.split('/')[0].strip(),
                                'start_game': cells[2].text.split('/')[1].strip(),
                                'end_elapsed': cells[3].text.split('/')[0].strip(),
                                'end_game': cells[3].text.split('/')[1].strip(),
                                'duration': cells[4].text,
                                'event': None if len(cells[5].text.strip()) == 0 else cells[5].text.strip()
                            }

                            self.toi[team][playername].append(shift)


class Rosters(NHLObject):
    def __init__(self, season, game_id):
        super(Rosters, self).__init__()
        self.season = season
        self.game_id = game_id
        self.roster = {}
        tables = {}
        
        url  = 'scores/htmlreports/%s/RO%s.HTM' % (season, game_id)
        soup = BeautifulSoup(self.geturl(url))
        
        try:
            maintable = soup.find_all('table', class_='tablewidth')[1]
            teamtable  = maintable.find_all('tr', recursive=False)[2].find('table')
            rostertable = maintable.find_all('tr', recursive=False)[3].find('table')

            visitor = teamtable('td')[0].text
            home = teamtable('td')[1].text
    
            tables['%s_dressed' % visitor] = rostertable.find('tr').find_all('td', recursive=False)[0].find('table')
            tables['%s_dressed' % home]    = rostertable.find('tr').find_all('td', recursive=False)[1].find('table')

            tables['%s_scratched' % visitor] = rostertable.find_all('tr', recursive=False)[3].find_all('table')[0]
            tables['%s_scratched' % home]    = rostertable.find_all('tr', recursive=False)[3].find_all('table')[1]
        except Exception as e:
            self.logmessage('Cannot parse roster report from %s (%s)' % (url, e), loglevel=logging.ERROR)
            return None

        for key in [visitor, home]:
            self.roster[key] = {'dressed': [], 'scratched': []}

            for status in self.roster[key].keys():
                table = tables['%s_%s' % (key, status)]
                for row in table.find_all('tr'):
                    cells = row.find_all('td')

                    if len(cells) == 2:
                        # Team
                        visitor = cells[0].text
                        home = cells[1].text
                    if len(cells) == 3:
                        # Player
                        jersey, pos, name = [c.text.strip() for c in cells]
                        for stripkey in ['(C)', '(A)']:
                            name = name.replace(stripkey, '').strip()
                        if name.find('Name') == -1:
                            self.roster[key][status].append({
                                'name': name,
                                'jersey': jersey,
                                'pos': pos
                            })


class Boxscore(NHLObject):
    def __init__(self, season, game_id):
        super(Boxscore, self).__init__()
        self.season = season
        self.game_id = game_id
        self.logs = {}

        url = 'gamecenter/boxscore?id=%s%s' % (season[:4], game_id)
        soup = BeautifulSoup(self.geturl(url))

        tables = soup.select('div.tableHeader')

        for header in tables:
            table = header.find_next('table')
            headers = [th.text for th in table.select('tr.sub')[0].find_all('th')]
            playertype = 'S' if header.text.find('skaters') >= 0 else 'G'
            team = header.text \
                         .replace('skaters', '') \
                         .replace('goaltenders', '') \
                         .strip().upper()
            
            if team not in self.logs:
                self.logs[team] = {'S': [], 'G': []}
            
            for row in table.select('tr.statsValues'):
                cells = row('td')
                playeranchor = cells[1].find('a')['href']
                d = dict(zip(headers,  [cell.text for cell in cells]))
                d['Player ID'] = re.search('=(\d+)$', playeranchor).groups()[0]
                
                for gk in ['EV', 'SH', 'PP', 'Saves - Shots']:
                    if gk in d:
                        d[gk] = [x.strip() for x in d[gk].split('-')]
                d = dict([(k, None if v == '-' else v) for (k,v) in d.items()])
                self.logs[team][playertype].append(d)


class Events(NHLObject):
    def __init__(self, season, game_id):
        super(Events, self).__init__()
        self.game_id = game_id
        self.season = season
        self.events = []

        try:
            url = '/GameData/%s/%s%s/PlayByPlay.json' % (season, season[:4], game_id)
            content = self.geturl(url, root='http://live.nhl.com').decode("utf-8")
            obj = json.loads(content)
            for event in obj['data']['game']['plays']['play']:
                self.events.append(event)
        except:
            pass
