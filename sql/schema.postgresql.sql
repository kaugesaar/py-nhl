-- STATS AND REPORTS
-- drop table if exists nhl.players cascade;
-- drop table if exists nhl.games cascade;
-- drop table if exists nhl.teams cascade;
-- drop table if exists nhl.players_names;
-- drop table if exists nhl.stats_skaters_summary;
-- drop table if exists nhl.stats_skaters_timeonice;
-- drop table if exists nhl.stats_skaters_faceoff;
-- drop table if exists nhl.stats_skaters_points;
-- drop table if exists nhl.stats_goalies_summary;
-- drop table if exists nhl.stats_goalies_special;
-- drop table if exists nhl.gamelogs_skaters;
-- drop table if exists nhl.gamelogs_goalies;
-- drop table if exists nhl.games_rosters;
-- drop table if exists nhl.games_faceoffs;
-- drop table if exists nhl.games_toi;
-- drop table if exists nhl.games_plays_players;
-- drop table if exists nhl.games_plays;
-- ICE TRACKER EVENTS
-- drop table if exists nhl.games_events cascade;
-- drop table if exists nhl.games_events_players;
-- drop table if exists nhl.games_events_penaltybox;

-- LOOKUPS

create table nhl.players_names (
    player_id integer, -- references nhl.players(player_id),
    player_name text,
    primary key (player_id, player_name)
);

create table nhl.teams (
    team text primary key,
    longname text,
    abbrev text,
    team_id integer unique,
    play_abbrev text unique, -- The abbreviation used in play by play
);

create table nhl.alignment (
    season text,
    team text references nhl.teams(team),
    division text,
    conference text,
    primary key (season, team, division, conference)
);

-- STATS AND REPORTS

create table nhl.players (
    player_id integer,
    jersey integer,
    player_name text,
    pos text,
    dob date,
    birthcity text,
    state text,
    country text,
    height integer,
    weight integer,
    hand text,
    primary key(player_id)
);

create table nhl.games (
    game_id text,
    season text,
    game_type integer,
    game_date date,
    visitor text,
    home text,
    vscore integer,
    hscore integer,
    overtime boolean,
    shootout boolean,
    attendance integer,
    primary key (season, game_id)
);

create table nhl.stats_skaters_summary (
    player_id integer references nhl.players(player_id),
    season text,
    game_type integer,
    gp integer,
    g integer,
    a integer,
    p integer,
    plusminus integer,
    pim integer,
    ppg integer,
    ppp integer,
    shg integer,
    shp integer,
    gw integer,
    ot integer,
    s integer,
    s_pct real,
    toi_g real,
    sft_g real,
    fo_pct real,
    primary key (player_id, season, game_type)
);

create table nhl.stats_skaters_timeonice (
    player_id integer references nhl.players(player_id),
    season text,
    game_type integer,
    gp integer,
    toi real,
    toi_g real,
    estoi real,
    estoi_g real,
    shtoi real,
    shtoi_g real,
    pptoi real,
    pptoi_g real,
    shifts integer,
    toi_shift real,
    shifts_g real,
    primary key (player_id, season, game_type)
);

create table nhl.stats_skaters_faceoff (
    player_id integer references nhl.players(player_id),
    season text,
    game_type integer,
    gp integer,
    fo integer,
    fow integer,
    fol integer,
    esfow integer,
    esfol integer,
    ppfow integer,
    ppfol integer,
    shfow integer,
    shfol integer,
    hfow integer,
    hfol integer,
    rfow integer,
    rfol integer,
    primary key (player_id, season, game_type)
);

create table nhl.stats_skaters_points (
    player_id integer references nhl.players(player_id),
    season text,
    game_type integer,
    gp integer,
    g integer,
    a integer,
    p integer,
    plusminus integer,
    esp integer,
    shp integer,
    ppp integer,
    hp integer,
    rp integer,
    dp integer,
    ndp integer,
    p_g real,
    primary key (player_id, season, game_type)
);

create table nhl.stats_goalies_summary (
    player_id integer references nhl.players(player_id),
    season text,
    game_type integer,
    gp integer,
    gs integer,
    w integer,
    l integer,
    ot integer,
    sa integer,
    ga integer,
    gaa real,
    sv integer,
    svpct real,
    so integer,
    g integer,
    a integer,
    pim integer,
    toi real,
    primary key (player_id, season, game_type)
);

create table nhl.stats_goalies_special (
    player_id integer references nhl.players(player_id),
    season text,
    game_type integer,
    gp integer,
    gs integer,
    ess integer,
    esg integer,
    essv integer,
    essvpct real,
    pps integer,
    ppg integer,
    ppsv integer,
    ppsvpct real,
    shs integer,
    shg integer,
    shsv integer,
    shsvpct real,
    otgames integer,
    ots integer,
    otg integer,
    otsvpct real,
    otgaa real,
    primary key (player_id, season, game_type)
);

create table nhl.gamelogs_skaters (
    season text not null,
    game_id text not null,
    player_id integer references nhl.players(player_id),
    team text,
    pos text,
    g integer,
    a integer,
    p integer,
    plusminus integer,
    pim integer,
    shots integer,
    hits integer,
    blocks integer,
    giveaways integer,
    takeaways integer,
    faceoff_pct real,
    pp_toi real,
    sh_toi real,
    toi real,
    primary key (season, game_id, player_id),
    foreign key (season, game_id) references nhl.games(season, game_id)
);

create table nhl.gamelogs_goalies (
    season text not null,
    game_id text not null,
    player_id integer references nhl.players(player_id),
    team text,
    evenstrength_saves integer,
    evenstrength_att integer,
    powerplay_saves integer,
    powerplay_att integer,
    shorthanded_saves integer,
    shorthanded_att integer,
    saves integer,
    att integer,
    save_pct real,
    pim integer,
    toi real,
    primary key (season, game_id, player_id),
    foreign key (season, game_id) references nhl.games(season, game_id)
);

create table nhl.games_rosters (
    season text not null,
    game_id text not null,
    player_id integer not null references nhl.players(player_id),
    team text,
    status text,
    jersey integer,
    pos text,
    primary key (season, game_id, player_id),
    foreign key (season, game_id) references nhl.games(season, game_id)
);

create table nhl.games_faceoffs (
    season text not null,
    game_id text not null,
    player_id integer not null references nhl.players(player_id),
    versus integer not null references nhl.players(player_id),
    zone text,
    wins integer,
    attempts integer,
    primary key (season, game_id, player_id, versus, zone),
    foreign key (season, game_id) references nhl.games(season, game_id)
);

create table nhl.games_toi (
    season text not null,
    game_id text not null,
    player_id integer not null references nhl.players(player_id),
    period integer,
    shift integer,
    start_elapsed real,
    start_game real,
    end_elapsed real,
    end_game real,
    duration real,
    event text,
    primary key (season, game_id, player_id, shift),
    foreign key (season, game_id) references nhl.games(season, game_id)
);

create table nhl.games_plays (
    season text not null,
    game_id text not null,
    eventno integer,
    period integer,
    strength text,
    time_elapsed real,
    time_game real,
    event_type text,
    description text,
    primary key (season, game_id, eventno),
    foreign key (season, game_id) references nhl.games(season, game_id)
);

create table nhl.games_plays_players (
    season text not null,
    game_id text not null,
    eventno integer,
    team text,
    longname text,
    player_id integer not null references nhl.players(player_id),
    pos text,
    primary key (season, game_id, eventno, player_id),
    foreign key (season, game_id, eventno) references nhl.games_plays(season, game_id, eventno),
    foreign key (season, game_id) references nhl.games(season, game_id),
    foreign key (longname) references nhl.teams(longname),
    foreign key (team) references nhl.teams(play_abbrev)
);

-- ICE TRACKER EVENTS

create table nhl.games_events (
    season text not null,
    game_id text not null,
    team_id integer references nhl.teams(team_id),
    event_id integer,
    formal_event_id text,
    period integer,
    strength integer,
    type text,
    shot_type text,
    description text,
    player_id integer,
    xcoord integer,
    ycoord integer,
    home_score integer,
    away_score integer,
    home_sog integer,
    away_sog integer,
    time text,
    video_url text,
    altvideo_url text,
    goalie_id integer,
    primary key (season, game_id, event_id),
    foreign key (season, game_id) references nhl.games(season, game_id)
);

create table nhl.games_events_players (
    season text not null,
    game_id text not null,
    event_id integer,
    player_id integer,
    which text,
    primary key (season, game_id, event_id, player_id),
    foreign key (season, game_id, event_id) references nhl.games_events(season, game_id, event_id),
    foreign key (season, game_id) references nhl.games(season, game_id)
);

create table nhl.games_events_penaltybox (
    season text not null,
    game_id text not null,
    event_id integer,
    player_id integer,
    which text,
    primary key (game_id, event_id, player_id),
    foreign key (season, game_id, event_id) references nhl.games_events(season, game_id, event_id),
    foreign key (season, game_id) references nhl.games(season, game_id)
);

/* indexes */

/*
create index idx_events_game_id on nhl.events(game_id);
create index idx_events_team_id on nhl.events(team_id);
create index idx_events_player_id on nhl.events(player_id);
create index idx_events_players_player_id on nhl.events_players(player_id);
create index idx_events_penaltybox_player_id on nhl.events_penaltybox(player_id);
create index idx_games_toi_combo on nhl.games_toi(game_id, period, shift);
create index idx_games_toi_combo2 on nhl.games_toi(game_id, period, start_elapsed);
*/