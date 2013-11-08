-- drop table if exists games;
-- drop table if exists teams;
-- drop table if exists events;
-- drop table if exists events_players;
-- drop table if exists events_penaltybox;
-- drop table if exists players;
-- drop table if exists stats_skaters_summary;
-- drop table if exists stats_skaters_timeonice;
-- drop table if exists stats_skaters_faceoff;
-- drop table if exists stats_skaters_points;
-- drop table if exists stats_goalies_summary;
-- drop table if exists stats_goalies_special;
-- drop table if exists gamelogs_skaters;
-- drop table if exists gamelogs_goalies;
-- drop table if exists games_rosters;
-- drop table if exists games_faceoffs;
-- drop table if exists games_toi;

/* USED BY events.py */

create table teams (
    team_id integer,
    name varchar(35),
    nickname varchar(35),
    primary key(team_id)
) engine = InnoDB;

create table games (
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
) engine = InnoDB;

create table events (
    event_id integer,
    formal_event_id varchar(15),
    game_id integer references games(game_id),
    period integer,
    strength integer,
    type varchar(15),
    shot_type varchar(15),
    description varchar(255),
    player_id integer,
    team_id integer references teams(team_id),
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
) engine = InnoDB;

create table events_players (
    game_id integer,
    event_id integer,
    which varchar(15),
    player_id integer
) engine = InnoDB;

create table events_penaltybox (
    game_id integer,
    event_id integer,
    which varchar(15),
    player_id integer
) engine = InnoDB;

/* USED BY stats.py */

create table players (
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
) engine = InnoDB;

create table stats_skaters_summary (
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
    s_pct float,
    toi_g float,
    sft_g float,
    fo_pct float,
    primary key (player_id, season)
) engine = InnoDB;

create table stats_skaters_timeonice (
    player_id integer references nhl.players(player_id),
    season integer,
    gp integer,
    evenstrength float,
    evenstrength_g float,
    shorthanded float,
    shorthanded_g float,
    powerplay float,
    powerplay_g float,
    total float,
    total_g float,
    shifts integer,
    total_s float,
    shifts_g float,
    primary key (player_id, season)
) engine = InnoDB;

create table stats_skaters_faceoff (
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
) engine = InnoDB;

create table stats_skaters_points (
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
    p_g float,
    primary key (player_id, season)
) engine = InnoDB;

create table stats_goalies_summary (
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
    sv_pct float,
    so integer,
    g integer,
    a integer,
    pim integer,
    toi float,
    primary key (player_id, season)
) engine = InnoDB;

create table stats_goalies_special (
    player_id integer references nhl.players(player_id),
    season integer,
    gp integer,
    gs integer,
    even_shots integer,
    even_goals integer,
    even_saves integer,
    even_save_pct float,
    pp_shots integer,
    pp_goals integer,
    pp_saves integer,
    pp_save_pct float,
    sh_shots integer,
    sh_goals integer,
    sh_saves integer,
    sh_save_pct float,
    ot_games integer,
    ot_shots integer,
    ot_goals integer,
    ot_save_pct float,
    ot_gaa float,
    primary key (player_id, season)
) engine = InnoDB;

create table gamelogs_skaters (
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
    faceoff_pct float,
    pp_toi float,
    sh_toi float,
    toi float,
    primary key (player_id, game_id)
) engine = InnoDB;

create table gamelogs_goalies (
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
    save_pct float,
    pim integer,
    toi float
) engine = InnoDB;

create table games_rosters (
    game_id integer not null references nhl.games(game_id),
    team text,
    status text,
    player_id integer not null
) engine = InnoDB;

create table games_faceoffs (
    game_id integer not null references nhl.games(game_id),
    player_id integer not null references nhl.players(player_id),
    versus integer not null references nhl.players(player_id),
    zone text,
    wins integer,
    attempts integer
) engine = InnoDB;

create table nhl.games_toi (
    game_id integer not null references nhl.games(game_id),
    player_id integer not null references nhl.players(player_id),
    period integer,
    shift integer,
    start_elapsed float,
    start_game float,
    end_elapsed float,
    end_game float,
    duration float,
    event text
) engine = InnoDB;