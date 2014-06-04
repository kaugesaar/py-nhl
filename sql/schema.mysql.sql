-- STATS AND REPORTS
drop table if exists players cascade;
drop table if exists games cascade;
drop table if exists teams cascade;
drop table if exists alignment cascade;
drop table if exists players_names;
drop table if exists stats_skaters_summary;
drop table if exists stats_skaters_timeonice;
drop table if exists stats_skaters_faceoff;
drop table if exists stats_skaters_points;
drop table if exists stats_goalies_summary;
drop table if exists stats_goalies_special;
drop table if exists gamelogs_skaters;
drop table if exists gamelogs_goalies;
drop table if exists games_rosters;
drop table if exists games_faceoffs;
drop table if exists games_toi;
drop table if exists games_plays cascade;
drop table if exists games_plays_players;
-- ICE TRACKER EVENTS
drop table if exists games_events_players;
drop table if exists games_events_penaltybox;
drop table if exists games_events;

-- LOOKUPS

create table players_names (
    player_id integer, -- references players(player_id),
    player_name varchar(255),
    primary key (player_id, player_name)
) engine = InnoDB CHARSET=utf8;

create table teams (
    team varchar(100) primary key,
    longname varchar(100),
    abbrev varchar(5),
    team_id integer unique,
    nickname varchar(100)
) engine = InnoDB CHARSET=utf8;

create table alignment (
    season varchar(10),
    team varchar(100) references teams(team),
    division varchar(100),
    conference varchar(100),
    primary key (season, team, division, conference)
) engine = InnoDB CHARSET=utf8;

-- STATS AND REPORTS

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
) engine = InnoDB CHARSET=utf8;

create table games (
    game_id varchar(10) not null,
    season varchar(10) not null,
    game_type integer,
    game_date date,
    visitor varchar(100),
    home varchar(100),
    vscore integer,
    hscore integer,
    overtime boolean,
    shootout boolean,
    attendance integer,
    index (game_id),
    index (season),
    primary key (game_id, season)
) engine = InnoDB CHARSET=utf8;

create table stats_skaters_summary (
    player_id integer references players(player_id),
    season varchar(10),
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
    s_pct float,
    toi_g float,
    sft_g float,
    fo_pct float,
    primary key (player_id, season, game_type)
) engine = InnoDB CHARSET=utf8;

create table stats_skaters_timeonice (
    player_id integer references players(player_id),
    season varchar(10),
    game_type integer,
    gp integer,
    toi float,
    toi_g float,
    estoi float,
    estoi_g float,
    shtoi float,
    shtoi_g float,
    pptoi float,
    pptoi_g float,
    shifts integer,
    toi_shift float,
    shifts_g float,
    primary key (player_id, season, game_type)
) engine = InnoDB CHARSET=utf8;

create table stats_skaters_faceoff (
    player_id integer references players(player_id),
    season varchar(10),
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
) engine = InnoDB CHARSET=utf8;

create table stats_skaters_points (
    player_id integer references players(player_id),
    season varchar(10),
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
    p_g float,
    primary key (player_id, season, game_type)
) engine = InnoDB CHARSET=utf8;

create table stats_goalies_summary (
    player_id integer references players(player_id),
    season varchar(10),
    game_type integer,
    gp integer,
    gs integer,
    w integer,
    l integer,
    ot integer,
    sa integer,
    ga integer,
    gaa float,
    sv integer,
    svpct float,
    so integer,
    g integer,
    a integer,
    pim integer,
    toi float,
    primary key (player_id, season, game_type)
) engine = InnoDB CHARSET=utf8;

create table stats_goalies_special (
    player_id integer references players(player_id),
    season varchar(10),
    game_type integer,
    gp integer,
    gs integer,
    ess integer,
    esg integer,
    essv integer,
    essvpct float,
    pps integer,
    ppg integer,
    ppsv integer,
    ppsvpct float,
    shs integer,
    shg integer,
    shsv integer,
    shsvpct float,
    otgames integer,
    ots integer,
    otg integer,
    otsvpct float,
    otgaa float,
    primary key (player_id, season, game_type)
) engine = InnoDB CHARSET=utf8;

create table gamelogs_skaters (
    season varchar(10) not null,
    game_id varchar(10) not null,
    player_id integer not null references players(player_id),
    team varchar(100),
    pos varchar(10),
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
    index (game_id),
    index (season),
    primary key (season, game_id, player_id),
    foreign key (season, game_id) references games(season, game_id)
) engine = InnoDB CHARSET=utf8;

create table gamelogs_goalies (
    season varchar(10) not null,
    game_id varchar(10) not null,
    player_id integer not null references players(player_id),
    team varchar(100),
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
    toi float,
    primary key (season, game_id, player_id),
    foreign key (season, game_id) references games(season, game_id)
) engine = InnoDB CHARSET=utf8;

create table games_rosters (
    season varchar(10) not null,
    game_id varchar(10) not null,
    player_id integer not null references players(player_id),
    team varchar(100),
    status varchar(100),
    jersey integer,
    pos varchar(3),
    primary key (season, game_id, player_id),
    foreign key (season, game_id) references games(season, game_id)
) engine = InnoDB CHARSET=utf8;

create table games_faceoffs (
    season varchar(10) not null,
    game_id varchar(10) not null,
    player_id integer not null references players(player_id),
    versus integer not null references players(player_id),
    zone varchar(5),
    wins integer,
    attempts integer,
    primary key (season, game_id, player_id, versus, zone),
    foreign key (season, game_id) references games(season, game_id)
) engine = InnoDB CHARSET=utf8;

create table games_toi (
    season varchar(10) not null,
    game_id varchar(10) not null,
    player_id integer not null references players(player_id),
    period integer,
    shift integer,
    start_elapsed float,
    start_game float,
    end_elapsed float,
    end_game float,
    duration float,
    event varchar(255),
    primary key (season, game_id, player_id, shift),
    foreign key (season, game_id) references games(season, game_id)
) engine = InnoDB CHARSET=utf8;

create table games_plays (
    season varchar(10) not null,
    game_id varchar(10) not null,
    eventno integer,
    period integer,
    strength text,
    time_elapsed float,
    time_game float,
    event_type varchar(255),
    description varchar(255),
    index (game_id),
    index (season),
    primary key (season, game_id, eventno),
    foreign key (season, game_id) references games(season, game_id)
) engine = InnoDB CHARSET=utf8;

create table games_plays_players (
    season varchar(10) not null,
    game_id varchar(10) not null,
    eventno integer,
    team varchar(100),
    longname varchar(100),
    player_id integer not null references players(player_id),
    pos varchar(5),
    index (game_id),
    index (season),
    primary key (season, game_id, eventno, player_id),
    foreign key (season, game_id, eventno) references games_plays(season, game_id, eventno),
    foreign key (season, game_id) references games(season, game_id)
) engine = InnoDB CHARSET=utf8;

-- ICE TRACKER EVENTS

create table games_events (
    season varchar(10) not null,
    game_id varchar(10) not null,
    event_id integer,
    formal_event_id varchar(15),
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
    primary key (game_id, event_id),
    foreign key (season, game_id) references games(season, game_id)
) engine = InnoDB CHARSET=utf8;

create table games_events_players (
    season varchar(10) not null,
    game_id varchar(10) not null,
    event_id integer,
    which varchar(15),
    player_id integer,
    primary key (season, game_id, event_id, player_id),
    foreign key (season, game_id, event_id) references games_events(season, game_id, event_id),
    foreign key (season, game_id) references games(season, game_id)
) engine = InnoDB CHARSET=utf8;

create table games_events_penaltybox (
    season varchar(10) not null,
    game_id varchar(10) not null,
    event_id integer,
    player_id integer,
    which varchar(15),
    primary key (game_id, event_id, player_id),
    foreign key (season, game_id, event_id) references games_events(season, game_id, event_id),
    foreign key (season, game_id) references games(season, game_id)
) engine = InnoDB CHARSET=utf8;