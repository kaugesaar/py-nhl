\echo 'Games'
select
    season,
    game_type,
    count(*) c
from nhl.games
group by season, game_type
order by season asc;

\echo 'Skaters - summary'
select
    season,
    game_type,
    count(*) c
from nhl.stats_skaters_summary
group by season, game_type
order by season asc;

\echo 'Skaters - faceoff'
select
    season,
    game_type,
    count(*) c
from nhl.stats_skaters_faceoff
group by season, game_type
order by season asc;

\echo 'Skaters - points'
select
    season,
    game_type,
    count(*) c
from nhl.stats_skaters_points
group by season, game_type
order by season asc;

\echo 'Skaters - TOI'
select
    season,
    game_type,
    count(*) c
from nhl.stats_skaters_timeonice
group by season, game_type
order by season asc;

\echo 'Game rosters'
select
    games.season,
    game_type,
    count(distinct game_id) c
from nhl.games_rosters
join nhl.games using (season, game_id)
group by games.season, game_type
order by games.season asc;

\echo 'Faceoffs'
select
    games.season,
    game_type,
    count(distinct game_id) c
from nhl.games_faceoffs
join nhl.games using (season, game_id)
group by games.season, game_type
order by games.season asc;

\echo 'TOI'
select
    games.season,
    game_type,
    count(distinct game_id) c
from nhl.games_toi
join nhl.games using (season, game_id)
group by games.season, game_type
order by games.season asc;

\echo 'Play by play'
select
    games.season,
    game_type,
    count(distinct game_id) c
from nhl.games_plays
join nhl.games using (season, game_id)
group by games.season, game_type
order by games.season asc;

\echo 'Play by play - on ice'
select
    games.season,
    game_type,
    count(distinct game_id) c
from nhl.games_plays_players
join nhl.games using (season, game_id)
group by games.season, game_type
order by games.season asc;

\echo 'Game logs - goalies'
select
    games.season,
    game_type,
    count(distinct game_id) c
from nhl.gamelogs_goalies
join nhl.games using (season, game_id)
group by games.season, game_type
order by games.season asc;

\echo 'Game logs - skaters'
select
    games.season,
    game_type,
    count(distinct game_id) c
from nhl.gamelogs_skaters
join nhl.games using (season, game_id)
group by games.season, game_type
order by games.season asc;

\echo 'Games plays'
select
    games.season,
    game_type,
    count(games_plays.*)
from nhl.games_plays
join nhl.games using (season, game_id)
group by games.season, game_type
order by games.season asc;

\echo 'Games plays - players'
select
    games.season,
    game_type,
    count(games_plays_players.*)
from nhl.games_plays_players
join nhl.games using (season, game_id)
group by games.season, game_type
order by games.season asc;

\echo 'Ice Tracker Events'
select
    games.season,
    game_type,
    count(distinct game_id) c
from nhl.games_events
join nhl.games using (season, game_id)
group by games.season, game_type
order by games.season asc;

\echo 'Ice Tracker Events - players'
select
    games.season,
    game_type,
    count(distinct game_id) c
from nhl.games_events_players
join nhl.games using (season, game_id)
group by games.season, game_type
order by games.season asc;

\echo 'Ice Tracker Events - penalty box'
select
    games.season,
    game_type,
    count(distinct game_id) c
from nhl.games_events_penaltybox
join nhl.games using (season, game_id)
group by games.season, game_type
order by games.season asc;

