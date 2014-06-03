from nhlcom import mapping, stats, reports, parse_time
from pprint import pprint
from sqlalchemy import Table, MetaData, and_, or_, distinct, func
from sqlalchemy.orm import sessionmaker, Mapper, join, outerjoin
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.sql.expression import extract
from datetime import datetime, timedelta

import sqlalchemy

engine = sqlalchemy.create_engine('postgresql://localhost/hockey')
meta = MetaData(bind=engine)
meta.reflect(bind=engine, schema='nhl')
Base = automap_base(metadata=meta)
Base.prepare(engine, reflect=True)
Classes = Base.classes

Session = sessionmaker(bind=engine)
session = Session()

Playermap = {}

def check(val):
    return None if val == '' else val


def get_player_id(player_name):
    global session, Base, Classes, Playermap # Globals? Like 'em? Hate 'em?
    
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
    session.query(players).filter(players.game_id == game_id).delete()
    session.query(plays).filter(plays.game_id == game_id).delete()

    for period, events in report.periods.items():
        for event in events:
            fields = mapping.fieldmap['games_plays'].items()
            params = {local: check(event[remote]) for local, remote in fields}
            obj = plays(**params)
            session.add(obj)
            
            for team in ['home', 'visitor']:
                for player in event['ice'][team]:
                    player_id = get_player_id(player['player'])
                    params = {
                        'game_id': game_id,
                        'eventno': event['eventno'],
                        'team': team,
                        'player_id': player_id
                    }
                    if player_id:
                        session.add(players(**params))
                    else:
                        print(players['player'], player_id)


def save_faceoffs(report):
    global session, Base, Classes

    game_id = report.game_id
    faceoffs = Classes.games_faceoffs
    session.query(faceoffs).filter(faceoffs.game_id == game_id).delete()
    
    for player_name, opponents in report.faceoffs.items():
        player_id = get_player_id(player_name)

        if not player_id:
            print('Cannot find player ID for name %s' % player_name.upper())
            continue

        for opp, zones in opponents.items():
            opponent = get_player_id(opp)
            if not opponent:
                print('Cannot find player ID for name %s' % player_name.upper())
                continue

            for zone, total  in zones.items():
                if len(total) > 1:
                    wins, attempts = total
                    params = {
                        'game_id': report.game_id,
                        'player_id': player_id,
                        'versus': opponent,
                        'zone': zone,
                        'wins': wins,
                        'attempts': attempts
                    }
                    session.add(faceoffs(**params))


def save_toi(report):
    global session, Base, Classes

    game_id = report.game_id
    toi = Classes.games_toi
    session.query(toi).filter(toi.game_id == game_id).delete()

    for team, players in report.toi.items():
        for player, shifts in players.items():
            player_id = get_player_id(player)

            if not player_id:
                print('Cannot find player ID for name %s' % player_name.upper())
                continue

            for shift in shifts:
                shift['game_id'] = report.game_id
                shift['player_id'] = player_id
                
                for key in ['duration', 'end_elapsed', 'end_game', 'start_elapsed', 'start_game']:
                    shift[key] = parse_time(shift[key])
                session.add(toi(**shift))


def save_roster(report):
    global session, Base, Classes

    game_id = report.game_id
    roster = Classes.games_rosters
    session.query(roster).filter(roster.game_id == game_id).delete()
    
    for team, statuses in report.roster.items():
        for status, players in statuses.items():
            for player in players:
                player_id = get_player_id(player)
                
                if not player_id:
                    print('Cannot find player ID for name %s' % player.upper())
                    continue
                
                params = {
                    'game_id': game_id,
                    'player_id': player_id,
                    'team': team,
                    'status': status
                }
                
                session.add(roster(**params))

def save_box(report):
    global session, Base, Classes
    
    game_id = report.game_id
    skaterlogs = Classes.gamelogs_skaters
    goalielogs = Classes.gamelogs_goalies
    
    session.query(skaterlogs).filter(skaterlogs.game_id == game_id).delete()
    session.query(goalielogs).filter(goalielogs.game_id == game_id).delete()
    
    for team, positions in report.logs.items():
        for pos, logs in positions.items():
            for log in logs:
                params = {
                    'game_id': game_id,
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
                    params['save_pct'] = log['Sv%'].replace('%', '')
                    params['pim'] = log['PIM']
                    params['toi'] = parse_time(log['TOI'])
                    real = {key: check(value) for key, value in params.items()}
                    if params['toi'] > 0:
                        session.add(goalielogs(**real))
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
                    params['faceoff_pct'] = log['FO%'].replace('-', '').replace('%', '')
                    params['pp_toi'] = parse_time(log['PP TOI'])
                    params['sh_toi'] = parse_time(log['SH TOI'])
                    params['toi'] = parse_time(log['TOI'])
                    real = {key: check(value) for key, value in params.items()}
                    session.add(skaterlogs(**real))


def save_events(report):
    global session, Base, Classes
    
    game_id = report.game_id
    
    e = Classes.games_events
    ep = Classes.games_events_players
    epb = Classes.games_events_penaltybox
    
    session.query(ep).filter(ep.game_id == game_id).delete()
    session.query(epb).filter(epb.game_id == game_id).delete()
    session.query(e).filter(e.game_id == game_id).delete()
    
    for event in report.events:
        fields = mapping.fieldmap['games_events'].items()
        params = {local: check(event[remote]) if remote in event else None for local, remote in fields}
        params['game_id'] = game_id
        obj = e(**params)
        session.add(obj)
        
        for key in ['aoi', 'hoi', 'hpb', 'apb']:
            if key in event:
                for player_id in event[key]:
                    params = {
                        'game_id': game_id,
                        'event_id': event['eventid'],
                        'player_id': player_id,
                        'which': 'visitor' if key in ['aoi', 'apb'] else 'home'
                    }
                    if key in ['aoi', 'hoi']:
                        session.add(ep(**params))
                    else:
                        session.add(epb(**params))

def parse_recent_games(season, game_type,
                       daysold=None, month=None, day=None, year=None,
                       game_id=None, limit=None):
    global session, Base, Classes

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

    print('parsing %s games for season %s (game type %s)' % \
        (count, season, game_type))

    for i, game in enumerate(query):
        print ('parsing game %s on date %s (%s/%s)' % \
            (game.game_id, game.game_date, i+1, count))
        # save_pbp(reports.PlayByPlay(game.season, game.game_id))
        # save_faceoffs(reports.Faceoffs(game.season, game.game_id))
        # save_toi(reports.TimeOnIce(game.season, game.game_id))
        # save_roster(reports.Rosters(game.season, game.game_id))
        # save_box(reports.Boxscore(game.season, game.game_id))
        save_events(reports.Events(game.season, game.game_id))


def parse_reports(season, game_type):
    games = stats.games('summary', **{'season': season, 'gameType': game_type})
    for game in games:
        game['Season'] = season
        game['Game Type'] = game_type
        game['Overtime'] = game['O/S'] == 'OT'
        game['Shootout'] = game['O/S'] == 'SO'
        fields = mapping.fieldmap['games'].items()
        params = {local: check(game[remote]) for local, remote in fields}
        obj = Base.classes.games(**params)

        if session.query(Base.classes.games).get(obj.game_id) is None:
            session.add(obj)

    for pos, tables in mapping.reportmap.items():
        for view in sorted(tables.keys()):
            table = tables[view]
            dbclass = Base.classes[table]

            if table != 'players':
                kw = {'season': season, 'game_type': game_type}
                session.query(dbclass).filter_by(**kw).delete()

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
                    pk = obj.player_id
                else:
                    pk = (obj.player_id, obj.season, obj.game_type)

                if session.query(dbclass).get(pk) is None:
                    session.add(obj)


if __name__ == '__main__':
    season = '20132014'
    
    for game_type in [2,3]:
        # parse_reports(season, game_type)
        # parse_recent_games(season, game_type, game_id='020083')
        parse_recent_games(season, game_type, month=10, day=30, year=2013)
        # parse_recent_games(season, game_type, full=True)
        # parse_recent_games(season, game_type, daysold=5)
        session.commit()
