from nhlcom import mapping, stats, reports, parse_time
from sqlalchemy import Table, MetaData, and_, or_, distinct, func
from sqlalchemy.orm import sessionmaker, Mapper, join, outerjoin
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.sql.expression import extract
from datetime import datetime, timedelta

import sqlalchemy
import logging
import sys
import configparser
import os

def check(val):
    return None if val == '' else val


def get_player_id(player_name):
    player_name = player_name.upper().strip()

    if player_name in Playermap:
        return Playermap[player_name]

    p = Classes.players
    pn = Classes.players_names

    query = session.query(p).outerjoin(pn, p.player_id == pn.player_id)
    orclause = or_ \
        ( \
            func.upper(p.player_name).like('%' + player_name + '%'), \
            func.upper(pn.player_name).like('%' + player_name + '%') \
        )
    res = query.filter(orclause).distinct(p.player_id)
    
    if res.count() == 0:
        return None

    player_id = res[0].player_id
    Playermap[player_name] = player_id
    return player_id


def save_pbp(report):
    global session, Base, Classes

    game_id = report.game_id
    plays = Classes.games_plays
    players = Classes.games_plays_players
    
    for period, events in report.periods.items():
        for event in events:
            fields = mapping.fieldmap['games_plays'].items()
            params = {local: check(event[remote]) for local, remote in fields}
            obj = plays(**params)
            session.merge(obj)
            
            for team, playerlist in event['ice'].items():
                for player in playerlist:
                    player_id = get_player_id(player['player'])
                    params = {
                        'season': report.season,
                        'game_id': game_id,
                        'eventno': event['eventno'],
                        'team': team,
                        'longname': player['longname'],
                        'player_id': player_id,
                        'pos': player['pos']
                    }
                    if player_id:
                        session.merge(players(**params))


def save_faceoffs(report):
    global session, Base, Classes
    
    logger = logging.getLogger("nhlcom")

    game_id = report.game_id
    faceoffs = Classes.games_faceoffs

    for player_name, opponents in report.faceoffs.items():
        player_id = get_player_id(player_name)

        if not player_id:
            logger.log(logging.ERROR, 'Cannot find player ID for name %s' % player_name.upper())
            continue

        for opp, zones in opponents.items():
            opponent = get_player_id(opp)
            if not opponent:
                logger.log(logging.ERROR, 'Cannot find player ID for name %s' % opp.upper())
                continue

            for zone, total  in zones.items():
                if len(total) > 1:
                    wins, attempts = total
                    params = {
                        'season': report.season,
                        'game_id': report.game_id,
                        'player_id': player_id,
                        'versus': opponent,
                        'zone': zone,
                        'wins': wins,
                        'attempts': attempts
                    }
                    session.merge(faceoffs(**params))


def save_toi(report):
    global session, Base, Classes

    logger = logging.getLogger("nhlcom")

    game_id = report.game_id
    toi = Classes.games_toi

    for team, players in report.toi.items():
        for player, shifts in players.items():
            player_id = get_player_id(player)

            if not player_id:
                logger.log(logging.ERROR, 'Cannot find player ID for name %s' % player.upper())
                continue

            for shift in shifts:
                shift['season'] = report.season
                shift['game_id'] = report.game_id
                shift['player_id'] = player_id
                
                for key in ['duration', 'end_elapsed', 'end_game', 'start_elapsed', 'start_game']:
                    shift[key] = parse_time(shift[key])
                session.merge(toi(**shift))


def save_roster(report):
    global session, Base, Classes

    logger = logging.getLogger("nhlcom")

    game_id = report.game_id
    roster = Classes.games_rosters

    for team, statuses in report.roster.items():
        for status, players in statuses.items():
            for player in players:
                player_id = get_player_id(player)
                
                if not player_id:
                    logger.log(logging.ERROR, 'Cannot find player ID for name %s' % player.upper())
                    continue
                
                params = {
                    'season': report.season,
                    'game_id': game_id,
                    'player_id': player_id,
                    'team': team,
                    'status': status
                }
                
                session.merge(roster(**params))


def save_box(report):
    global session, Base, Classes
    
    game_id = report.game_id
    skaterlogs = Classes.gamelogs_skaters
    goalielogs = Classes.gamelogs_goalies

    for team, positions in report.logs.items():
        for pos, logs in positions.items():
            for log in logs:
                params = {
                    'season': report.season,
                    'game_id': report.game_id,
                    'player_id': log['Player ID'],
                    'team': team,
                }

                if pos == 'G':
                    params['evenstrength_saves'] = log['EV'][0]
                    params['evenstrength_att'] = log['EV'][1]
                    params['powerplay_saves'] = log['PP'][0]
                    params['powerplay_att'] = log['PP'][1]
                    params['shorthanded_saves'] = log['SH'][0]
                    params['shorthanded_att'] = log['SH'][1]
                    params['saves'] = log['Saves - Shots'][0]
                    params['att'] = log['Saves - Shots'][1]
                    if log['Sv%']:
                        params['save_pct'] = log['Sv%'].replace('%', '')
                    else:
                        params['save_pct'] = None
                    params['pim'] = log['PIM']
                    params['toi'] = parse_time(log['TOI'])
                    real = {key: check(value) for key, value in params.items()}
                    if params['toi'] > 0:
                        session.merge(goalielogs(**real))
                elif pos == 'S':
                    params['g'] = log['G']
                    params['a'] = log['A']
                    params['p'] = log['P']
                    params['plusminus'] = log['+/-']
                    params['shots'] = log['S']
                    params['hits'] = log['Hits']
                    params['blocks'] = log['BkS']
                    params['giveaways'] = log['GvA']
                    params['takeaways'] = log['TkA']
                    if log['FO%']:
                        params['faceoff_pct'] = log['FO%'].replace('-', '').replace('%', '')
                    else:
                        params['faceoff_pct'] = None
                    params['pp_toi'] = parse_time(log['PP TOI'])
                    params['sh_toi'] = parse_time(log['SH TOI'])
                    params['toi'] = parse_time(log['TOI'])
                    real = {key: check(value) for key, value in params.items()}
                    session.merge(skaterlogs(**real))


def save_events(report):
    global session, Base, Classes
    
    game_id = report.game_id
    
    e = Classes.games_events
    ep = Classes.games_events_players
    epb = Classes.games_events_penaltybox

    for event in report.events:
        fields = mapping.fieldmap['games_events'].items()
        params = {local: check(event[remote]) if remote in event else None for local, remote in fields}
        params['game_id'] = game_id
        params['season'] = report.season
        obj = e(**params)
        session.merge(obj)
        
        for key in ['aoi', 'hoi', 'hpb', 'apb']:
            if key in event:
                for player_id in set(event[key]):
                    params = {
                        'season': report.season,
                        'game_id': game_id,
                        'event_id': event['eventid'],
                        'player_id': player_id,
                        'which': 'visitor' if key in ['aoi', 'apb'] else 'home'
                    }
                    if key in ['aoi', 'hoi']:
                        session.merge(ep(**params))
                    else:
                        session.merge(epb(**params))


def parse_recent_games(season, game_type,
                       daysold=None, month=None, day=None, year=None,
                       game_id=None, limit=None):
    global session, Base, Classes

    logger = logging.getLogger("nhlcom")

    games = Classes.games
    filters = [games.season == season, games.game_type == game_type]

    if month:
        filters.append(extract('month', games.game_date) == month)
    if day:
        filters.append(extract('day', games.game_date) == day)
    if year:
        filters.append(extract('year', games.game_date) == year)
    if daysold:
        then = datetime.today() - timedelta(days=daysold)
        filters.append(games.game_date >= then)
    if game_id:
        filters.append(games.game_id == game_id)

    query = session.query(games). \
        filter(and_(*filters)). \
        order_by(games.game_date.asc()). \
        limit(limit)
    
    count = query.count()
    
    logger.log(logging.INFO, 'parsing %s games for season %s (game type %s)' % \
        (count, season, game_type))

    for i, game in enumerate(query):
        logger.log(logging.INFO, 'parsing game %s on date %s (%s/%s)' % \
            (game.game_id, game.game_date, i+1, count))
        save_pbp(reports.PlayByPlay(game.season, game.game_id))
        save_faceoffs(reports.Faceoffs(game.season, game.game_id))
        save_toi(reports.TimeOnIce(game.season, game.game_id))
        save_roster(reports.Rosters(game.season, game.game_id))
        save_box(reports.Boxscore(game.season, game.game_id))
        save_events(reports.Events(game.season, game.game_id))


def parse_games(season, game_type):
    global session, Base, Classes

    games = stats.games('summary', **{'season': season, 'gameType': game_type})
    for game in games:
        game['Season'] = season
        game['Game Type'] = game_type
        game['Overtime'] = game['O/S'] == 'OT'
        game['Shootout'] = game['O/S'] == 'SO'
        fields = mapping.fieldmap['games'].items()
        params = {local: check(game[remote]) for local, remote in fields}
        session.merge(Classes.games(**params))


def parse_reports(season, game_type):
    global session, Base, Classes
    for pos, tables in mapping.reportmap.items():
        for view in sorted(tables.keys()):
            table = tables[view]
            dbclass = Classes[table]

            kw = {'season': season, 'gameType': game_type, 'position': pos}
            report = stats.players(view, pos=pos, **kw)

            for row in report:
                row['Season'] = season
                row['Game Type'] = game_type
                if view == 'goalieBios':
                    row['S'] = row['C']
                    row['Pos'] = 'G'

                items = mapping.fieldmap[table].items()
                params = {local: check(row[remote]) for local, remote in items}
                obj = dbclass(**params)
                
                if table == 'players':
                    if session.query(dbclass). \
                        filter(dbclass.player_id == obj.player_id). \
                        first():
                            continue

                session.merge(obj)


def main():
    global session, Base, Classes, Playermap # Globals? Like 'em? Hate 'em?

    pwd = os.path.dirname(__file__)
    if pwd == '': pwd = '.'
    config = configparser.ConfigParser()
    config.readfp(open('%s/py-nhl.ini' % pwd))
    
    ENGINE = config['database'].get('engine')
    HOST = config['database'].get('host')
    DATABASE = config['database'].get('database')
    SCHEMA = config['database'].get('schema')
    USER = config['database'].get('user')
    PASSWORD = config['database'].get('password')
    
    if not ENGINE or not HOST or not DATABASE:
        print('Need to define at least engine, host, and database')
        raise SystemExit

    if USER and PASSWORD: string = '%s://%s:%s@%s/%s' % (ENGINE, USER, PASSWORD, HOST, DATABASE)
    else:  string = '%s://%s/%s' % (ENGINE, HOST, DATABASE)
    
    engine = sqlalchemy.create_engine(string)
    meta = MetaData(bind=engine)
    
    if SCHEMA:
        meta.reflect(bind=engine, schema=SCHEMA)
    else:
        meta.reflect(bind=engine)
    
    Base = automap_base(metadata=meta)
    Base.prepare(engine, reflect=True)
    Classes = Base.classes
    
    Session = sessionmaker(bind=engine)
    session = Session()

    Playermap = {}

    dateformat = '%m/%d/%Y %I:%M %p'
    logformat = '%(levelname)s | %(asctime)s | %(name)s | %(message)s'
    formatter = logging.Formatter(logformat, datefmt=dateformat)

    s1 = logging.StreamHandler(stream=sys.stdout)
    s1.setLevel(logging.DEBUG)
    s1.setFormatter(formatter)

    # s2 = logging.StreamHandler(stream=sys.stderr)
    # s2.setLevel(logging.ERROR)
    # s2.setFormatter(formatter)

    logger = logging.getLogger('nhlcom')
    logger.addHandler(s1)
    logger.setLevel(logging.DEBUG)

    for season in ['20132014']:
        for game_type in [2,3]:
            parse_games(season, game_type)
            parse_reports(season, game_type)
            parse_recent_games(season, game_type, daysold=2)
            session.commit()
    logger.log(logging.INFO, 'All done!')


if __name__ == '__main__':
    main()
