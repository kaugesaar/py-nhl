from . import BaseReport, parse_time
from datetime import datetime
from pprint import pprint


import urllib.request, urllib.error, urllib.parse
import logging
import re


class players(BaseReport):
    def __init__(self, view, pos=None, maxpages=None, **kwargs):
        url = 'ice/playerstats.htm'
        parent = super(players, self)
        parent.__init__(url, view, pos=pos, maxpages=maxpages, **kwargs)

    def parse_headers(self, view_name, columns): # Really need the view here.
        cols = super(players, self).parse_headers(view_name, columns)
        
        if view_name == 'summary':
            cols[0] = 'n' # The row number in the report- who cares?
        
        if view_name in ['summary', 'faceOffPercentageAll', 'bios', 'goalieBios', 'timeOnIce', 'points', 'specialTeamSaves']:
            cols.append('Player ID') # We'll get the player ID
        return cols

    def parse_columns(self, view_name, columns):
        if view_name in ['summary', 'bios', 'goalieBios', 'faceOffPercentageAll', 'timeOnIce', 'points', 'specialTeamSaves']:
            href = columns[1].find('a')['href']
            columns.append(re.search('=(\d+)$', href).groups()[0])

    def parse_row(self, view_name, row):
        row = super(players, self).parse_row(view_name, row)
        
        if view_name in ['bios', 'goalieBios']:
            rawdate = re.sub(r'\W+','', row['DOB'])
            row['DOB'] = datetime.strptime(rawdate, '%b%d%y').date()
        
        toi_keys = ['TOI', 'TOI/G', 'ES TOI/G', 'PP TOI/G', 'SH TOI/G',
                    'PP TOI', 'SH TOI', 'ES TOI']
        num_keys = ['Shifts']
        for key in toi_keys:
            if key in row:
                row[key] = parse_time(row[key])
        for key in num_keys:
            if key in row:
                row[key] = int(row[key].replace(',', ''))

        return row


class games(BaseReport):
    def __init__(self, view, maxpages=None, **kwargs):
        url = 'ice/gamestats.htm'
        parent = super(games, self)
        parent.__init__(url, view, maxpages=maxpages, **kwargs)

    def parse_headers(self, view, columns):
        cols = super(games, self).parse_headers(view, columns)

        if view == 'summary':
            cols.append('Game ID') # We'll get the game ID
        return cols

    def parse_columns(self, view, columns):
        if view == 'summary':
            href = columns[0].find('a')['href']
            columns.append(re.search('GS(\d+)\.HTM$', href).groups()[0])

    def parse_row(self, view, row):
        if row['Att'] == '':
            return row # Game not completed

        rawdate = re.sub(r'\W+','', row['Date'])
        row['Date'] = datetime.strptime(rawdate, '%b%d%y').date()
        row['Att'] = int(re.sub(r'\W+', '', row['Att']))
        return row