\echo 'Games'
select
    season,
    count(*) c
from nhl.games
group by season
order by season asc;

\echo 'Game rosters'
select
    season,
    count(distinct game_id) c
from nhl.games_rosters
join nhl.games using (game_id)
group by season
order by season asc;

\echo 'Faceoffs'
select
    season,
    count(distinct game_id) c
from nhl.games_faceoffs
join nhl.games using (game_id)
group by season
order by season asc;

\echo 'Game logs - goalies'
select
    season,
    count(distinct game_id) c
from nhl.gamelogs_goalies
join nhl.games using (game_id)
group by season
order by season asc;

\echo 'Game logs - skaters'
select
    season,
    count(distinct game_id) c
from nhl.gamelogs_skaters
join nhl.games using (game_id)
group by season
order by season asc;

