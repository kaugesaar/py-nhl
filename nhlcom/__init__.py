from . import mapping

from bs4 import BeautifulSoup, Tag
from pprint import pprint

import logging
import urllib.request, urllib.error, urllib.parse
import re

__version__ = '1.0'

NHL_URL = 'http://www.nhl.com'

def parse_time(time):
    if time is None: return None
    m,s = time.replace(',', '').split(':')
    return round(int(m) + (int(s) / 60.0), 2)

class NHLObject:
    def __init__(self, timeout=30):
        self.timeout=timeout
    
    def logmessage(self, message, **kwargs):
        logger = logging.getLogger('nhlcom')
        loglevel = kwargs.get('loglevel', logging.INFO)
        logger.log(loglevel, '%s: %s' % (self.__class__.__name__, message))

    def geturl(self, url, root=None, **kwargs):
        urlroot = NHL_URL if not root else root
        if kwargs:
            querystring = urllib.parse.urlencode(kwargs)
            url = '%s/%s?%s'  % (urlroot, url, querystring)
        else:
            url = '%s/%s'  % (urlroot, url)

        try:
            self.logmessage('fetching %s' % url)
            headers = {'User-Agent': 'KopitarBot 1.0'}
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-Agent', 'KopitarBot %s' % __version__)]
            res = opener.open(url, timeout=self.timeout)
            return res.read()
        except urllib.error.HTTPError as e:
            msg = 'error code %s on %s' % (e.code, url)
            self.logmessage(msg, loglevel=logging.ERROR)
            return None
        except urllib.error.URLError as e:
            msg = 'bailing on %s (timeout of %s exceeded)' % (url, timeout)
            self.logmessage(msg, loglevel=logging.ERROR)
            return None


class BaseReport(NHLObject):
    def __init__(self, url, view_name, pos=None, maxpages=None, timeout=30, **kwargs):
        super(BaseReport, self).__init__(timeout=timeout)
        self.maxpages = maxpages
        self.timeout = timeout
        self.pageURL = url
        self.headers = []
        self.rows = []
        self.view_name = view_name
        self.pos = pos
        self.fetch(**kwargs)

    def __len__(self):
        return len(self.rows)

    def __iter__(self):
        return iter(self.rows)

    def __getitem__(self, key):
        return self.rows[key]

    def parse_row(self, view_name, row):
        """
        Can be overriden to reformat the report's rows
        """
        return row

    def parse_headers(self, view_name, columns):
        """
        NHL.com uses duplicate column names so let's appemd a ", x"
        where there are multiples
        """
        cols = []
        counts = {}

        for col in columns:
            val = col.text.strip()
            if val in cols:
                if val not in counts:
                    counts[val] = 1
                else:
                    counts[val] += 1
                val = '%s, %d' % (val, counts[val])
            cols.append(val)
        return cols

    # Can be overriden to handle the raw HTML
    def parse_columns(self, view_name, columns):
        """
        If access is needed to the raw HTML to e.g. pull player ID values
        from the anchor tag attributes
        """
        pass

    def persist(self, item):
        """
        Does nothing yet but will soon enough do the DB-saving
        """
        if isinstance(self, stats.games):
            m = mapping.fieldmap['games']
        elif isinstance(self, stats.players):
            m = mapping.fieldmap[self.pos][self.view_name]
        pass # Not implemented yet

    def fetch(self, **kwargs):
        kwargs['viewName'] = self.view_name
        
        if self.maxpages is None:
            # Need to get maximum number of pages
            res = self.geturl(self.pageURL, **kwargs)
        
            if res is None:
                return False
        
            soup = BeautifulSoup(res)
            
            if soup is None:
                return False
        
            try:
                div = soup.find('div', 'pages')
                last_anchor = div.find_all('a')[-1]
                parts = urllib.parse.parse_qs(last_anchor['href'])
                self.maxpages = int(parts['pg'][0])
            except Exception as e:
                self.maxpages = 1
        
        for page in range(1, self.maxpages + 1):
            kwargs['pg'] = page
            res = self.geturl(self.pageURL, **kwargs)
            soup = BeautifulSoup(res)
            
            if soup is None:
                return
            
            table = soup.find('table', class_='stats')
            header = table.find('thead').find_all('th')
            body = table.find('tbody').find_all('tr')

            self.headers = self.parse_headers(self.view_name, header)
        
            for row in body:
                tablecolumns = row.find_all('td')
                self.parse_columns(self.view_name, tablecolumns)
                columns = []
                
                for col in tablecolumns:
                    if type(col) is Tag:
                        columns.append(col.text.strip())
                    else:
                        columns.append(col)
                
                item = dict(zip(self.headers, columns))
                self.rows.append(self.parse_row(self.view_name, item))
