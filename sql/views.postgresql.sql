begin;

drop view if exists nhl.vw_skaters_summary;
drop view if exists nhl.vw_faceoffs;
drop view if exists nhl.vw_games_toi;

create view nhl.vw_skaters_summary as
select
    s.season,
    s.player_id,
    p.player_name,
    p.pos,
    extract(year from age(('01-01-'||substring(season::text from 5))::date, p.dob)) as age,
    s.gp,
    s.g,
    s.a,
    s.p,
    s.plusminus,
    s.pim,
    s.pp as ppg,
    s.sh as shg,
    s.gw as gwg,
    s.ot as otg,
    s.s,
    s.s_pct,
    s.sft_g as shiftf_g,
    f.fow + f.fol as fo,
    f.fow,
    f.fol,
    s.fo_pct,
    f.evenstrength_fow,
    f.evenstrength_fol,
    case
        when (f.evenstrength_fow + f.evenstrength_fol) = 0 then null else
        round(f.evenstrength_fow / (f.evenstrength_fow + f.evenstrength_fol)::numeric * 100, 1)
    end as evenstrength_fo_pct,
    f.powerplay_fow,
    f.powerplay_fol,
    case
        when (f.powerplay_fow + f.powerplay_fol) = 0 then null else
        round(f.powerplay_fow / (f.powerplay_fow + f.powerplay_fol)::numeric * 100, 1)
    end as powerplay_fo_pct,
    f.shorthanded_fow,
    f.shorthanded_fol,
    case
        when (f.shorthanded_fow + f.shorthanded_fol) = 0 then null else
        round(f.shorthanded_fow / (f.shorthanded_fow + f.shorthanded_fol)::numeric * 100, 1)
    end as shorthanded_fo_pct,
    h.hits,
    t.evenstrength as evenstrength_toi,
    t.evenstrength_g evenstrength_toi_g,
    t.shorthanded as shorthanded_toi,
    t.shorthanded_g shorthanded_toi_g,
    t.powerplay as powerplay_toi,
    t.powerplay_g as powerplay_toi_g,
    t.total as toi,
    t.total_g toi_g,
    t.shifts,
    t.total_s shifts_toi,
    t.shifts_g
from nhl.stats_skaters_summary s
join nhl.players p using (player_id)
left join nhl.stats_skaters_faceoff f using (player_id, season)
left join nhl.stats_skaters_hits h using (player_id, season)
left join nhl.stats_skaters_timeonice t using (player_id, season);

create view nhl.vw_faceoffs as
select
    season,
    player_name,
    "zone",
    sum(f.wins) wins,
    sum(f.attempts) attempts,
    case when sum(f.attempts) = 0 then null else round(sum(f.wins) / sum(f.attempts)::numeric * 100, 1) end as pct
from nhl.games_faceoffs f
join nhl.games g using (game_id)
join nhl.players p using (player_id)
group by season, player_name, "zone";

create view nhl.vw_games_toi as
select
    season,
    game_id,
    player_id,
    player_name,
    r.team,
    case when r.team = h.long then h.team_id else v.team_id end as team_id,
    case when r.team = h.long then 'home' else 'visitor' end as teamtype,
    period,
    shift,
    start_elapsed,
    start_game,
    end_elapsed,
    end_game,
    duration,
    event
from nhl.games_toi t
join nhl.games_rosters r using (game_id, player_id)
join nhl.games g using (game_id)
join nhl.players p using (player_id)
join nhl.teams h on (g.home = h.team)
join nhl.teams v on (g.visitor = v.team);

commit;