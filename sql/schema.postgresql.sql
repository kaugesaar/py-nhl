-- drop table if exists nhl.players cascade;
-- drop table if exists nhl.games cascade;
-- drop table if exists nhl.stats_skaters_summary;
-- drop table if exists nhl.stats_skaters_summary;
-- drop table if exists nhl.stats_skaters_timeonice;
-- drop table if exists nhl.stats_skaters_faceoff;
-- drop table if exists nhl.stats_skaters_points;
-- drop table if exists nhl.stats_goalies_summary;
-- drop table if exists nhl.stats_goalies_special;
-- drop table if exists nhl.gamelogs_skaters;
-- drop table if exists nhl.gamelogs_goalies;
-- drop table if exists nhl.events cascade;
-- drop table if exists nhl.events_players;
-- drop table if exists nhl.events_penaltybox;

/* USED BY stats.py */

create table nhl.players (
    player_id integer,
    jersey integer,
    player_name varchar(100),
    pos varchar(3),
    dob date,
    birthcity varchar(100),
    state varchar(10),
    country varchar(10),
    height integer,
    weight integer,
    hand char,
    primary key(player_id)
);

create table nhl.games (
    game_id integer primary key,
    season integer,
    game_date date,
    visitor text,
    home text,
    visitor_score integer,
    home_score integer,
    overtime boolean,
    shootout boolean,
    attendance integer
);

create table nhl.stats_skaters_summary (
    player_id integer references nhl.players(player_id),
    season integer,
    gp integer,
    g integer,
    a integer,
    p integer,
    plusminus integer,
    pim integer,
    pp integer,
    sh integer,
    gw integer,
    ot integer,
    s integer,
    s_pct numeric,
    toi_g numeric,
    sft_g numeric,
    fo_pct numeric,
    primary key (player_id, season)
);

create table nhl.stats_skaters_timeonice (
    player_id integer references nhl.players(player_id),
    season integer,
    gp integer,
    evenstrength numeric,
    evenstrength_g numeric,
    shorthanded numeric,
    shorthanded_g numeric,
    powerplay numeric,
    powerplay_g numeric,
    total numeric,
    total_g numeric,
    shifts integer,
    total_s numeric,
    shifts_g numeric,
    primary key (player_id, season)
);

create table nhl.stats_skaters_faceoff (
    player_id integer references nhl.players(player_id),
    season integer,
    gp integer,
    evenstrength_fow integer,
    evenstrength_fol integer,
    powerplay_fow integer,
    powerplay_fol integer,
    shorthanded_fow integer,
    shorthanded_fol integer,
    home_fow integer,
    home_fol integer,
    road_fow integer,
    road_fol integer,
    fow integer,
    fol integer,
    total integer,
    primary key (player_id, season)
);

create table nhl.stats_skaters_points (
    player_id integer references nhl.players(player_id),
    season integer,
    gp integer,
    g integer,
    a integer,
    p integer,
    plusminus integer,
    evenstrength_p integer,
    shorthanded_p integer,
    powerplay_p integer,
    home_p integer,
    away_p integer,
    division_p integer,
    nondivision_p integer,
    p_g numeric,
    primary key (player_id, season)
);

create table nhl.stats_goalies_summary (
    player_id integer references nhl.players(player_id),
    season integer,
    gp integer,
    gs integer,
    w integer,
    l integer,
    ot integer,
    sa integer,
    ga integer,
    gaa real,
    sv integer,
    sv_pct numeric,
    so integer,
    g integer,
    a integer,
    pim integer,
    toi numeric,
    primary key (player_id, season)
);

create table nhl.stats_goalies_special (
    player_id integer references nhl.players(player_id),
    season integer,
    gp integer,
    gs integer,
    even_shots integer,
    even_goals integer,
    even_saves integer,
    even_save_pct numeric,
    pp_shots integer,
    pp_goals integer,
    pp_saves integer,
    pp_save_pct numeric,
    sh_shots integer,
    sh_goals integer,
    sh_saves integer,
    sh_save_pct numeric,
    ot_games integer,
    ot_shots integer,
    ot_goals integer,
    ot_save_pct numeric,
    ot_gaa numeric,
    primary key (player_id, season)
);

create table nhl.gamelogs_skaters (
    game_id integer not null references nhl.games(game_id),
    player_id integer,
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
    faceoff_pct numeric,
    pp_toi numeric,
    toi numeric,
    primary key (player_id, game_id)
);

create table nhl.gamelogs_goalies (
    game_id integer not null references nhl.games(game_id),
    player_id integer,
    team text,
    evenstrength_saves integer,
    evenstrength_att integer,
    powerplay_saves integer,
    powerplay_att integer,
    shorthanded_saves integer,
    shorthanded_att integer,
    saves integer,
    att integer,
    save_pct numeric,
    pim integer,
    toi numeric
);

/* USED BY events.py */

create table nhl.events (
    event_id integer,
    formal_event_id varchar(15),
    game_id integer references nhl.games(game_id),
    period integer,
    strength integer,
    type varchar(15),
    shot_type varchar(15),
    description varchar(255),
    player_id integer,
    team_id integer references nhl.teams(team_id),
    xcoord integer,
    ycoord integer,
    home_score integer,
    away_score integer,
    home_sog integer,
    away_sog integer,
    time varchar(10),
    video_url varchar(255),
    altvideo_url varchar(255),
    goalie_id integer,
    primary key (game_id, event_id)
);

create table nhl.events_players (
    game_id integer references nhl.games(game_id),
    event_id integer,
    which varchar(15),
    player_id integer,
    foreign key(game_id, event_id) references nhl.events(game_id, event_id)
);

create table nhl.events_penaltybox (
    game_id integer references nhl.games(game_id),
    event_id integer,
    which varchar(15),
    player_id integer,
    foreign key(game_id, event_id) references nhl.events(game_id, event_id)
);

/* indexes */

create index idx_events_game_id on events(game_id);
create index idx_events_team_id on events(team_id);
create index idx_events_player_id on events(player_id);
create index idx_events_players_player_id on events_players(player_id);
create index idx_events_penaltybox_player_id on events_penaltybox(player_id);
