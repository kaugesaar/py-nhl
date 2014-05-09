/*
*
* Contains all NHL teams as they appear in various reports
* mysql users: remove the SET call
*
*/

SET search_path to nhl;

DROP TABLE IF EXISTS teams;

CREATE TABLE teams (
    team text primary key,
    "long" text,
    abbrev text,
    team_id integer unique,
    nickname text
);


INSERT INTO teams (team, "long", abbrev, team_id, nickname) VALUES ('SAN JOSE', 'SAN JOSE SHARKS', 'SJS', 28, NULL);
INSERT INTO teams (team, "long", abbrev, team_id, nickname) VALUES ('ST LOUIS', 'ST. LOUIS BLUES', 'STL', 19, NULL);
INSERT INTO teams (team, "long", abbrev, team_id, nickname) VALUES ('TAMPA BAY', 'TAMPA BAY LIGHTNING', 'TBL', 14, NULL);
INSERT INTO teams (team, "long", abbrev, team_id, nickname) VALUES ('TORONTO', 'TORONTO MAPLE LEAFS', 'TOR', 10, NULL);
INSERT INTO teams (team, "long", abbrev, team_id, nickname) VALUES ('VANCOUVER', 'VANCOUVER CANUCKS', 'VAN', 23, NULL);
INSERT INTO teams (team, "long", abbrev, team_id, nickname) VALUES ('WASHINGTON', 'WASHINGTON CAPITALS', 'WSH', 15, NULL);
INSERT INTO teams (team, "long", abbrev, team_id, nickname) VALUES ('WINNIPEG', 'WINNIPEG JETS', 'WPG', 52, NULL);
INSERT INTO teams (team, "long", abbrev, team_id, nickname) VALUES ('ATLANTA', 'ATLANTA THRASHERS', 'ATL', NULL, NULL);
INSERT INTO teams (team, "long", abbrev, team_id, nickname) VALUES ('ANAHEIM', 'ANAHEIM DUCKS', 'ANA', 24, NULL);
INSERT INTO teams (team, "long", abbrev, team_id, nickname) VALUES ('BOSTON', 'BOSTON BRUINS', 'BOS', 6, NULL);
INSERT INTO teams (team, "long", abbrev, team_id, nickname) VALUES ('BUFFALO', 'BUFFALO SABRES', 'BUF', 7, NULL);
INSERT INTO teams (team, "long", abbrev, team_id, nickname) VALUES ('CALGARY', 'CALGARY FLAMES', 'CGY', 20, NULL);
INSERT INTO teams (team, "long", abbrev, team_id, nickname) VALUES ('CAROLINA', 'CAROLINA HURRICANES', 'CAR', 12, NULL);
INSERT INTO teams (team, "long", abbrev, team_id, nickname) VALUES ('CHICAGO', 'CHICAGO BLACKHAWKS', 'CHI', 16, NULL);
INSERT INTO teams (team, "long", abbrev, team_id, nickname) VALUES ('COLORADO', 'COLORADO AVALANCHE', 'COL', 21, NULL);
INSERT INTO teams (team, "long", abbrev, team_id, nickname) VALUES ('COLUMBUS', 'COLUMBUS BLUE JACKETS', 'CBJ', 29, NULL);
INSERT INTO teams (team, "long", abbrev, team_id, nickname) VALUES ('DALLAS', 'DALLAS STARS', 'DAL', 25, NULL);
INSERT INTO teams (team, "long", abbrev, team_id, nickname) VALUES ('DETROIT', 'DETROIT RED WINGS', 'DET', 17, NULL);
INSERT INTO teams (team, "long", abbrev, team_id, nickname) VALUES ('EDMONTON', 'EDMONTON OILERS', 'EDM', 22, NULL);
INSERT INTO teams (team, "long", abbrev, team_id, nickname) VALUES ('FLORIDA', 'FLORIDA PANTHERS', 'FLA', 13, NULL);
INSERT INTO teams (team, "long", abbrev, team_id, nickname) VALUES ('LOS ANGELES', 'LOS ANGELES KINGS', 'LAK', 26, NULL);
INSERT INTO teams (team, "long", abbrev, team_id, nickname) VALUES ('MINNESOTA', 'MINNESOTA WILD', 'MIN', 30, NULL);
INSERT INTO teams (team, "long", abbrev, team_id, nickname) VALUES ('MONTREAL', 'MONTRÉAL CANADIENS', 'MTL', 8, NULL);
INSERT INTO teams (team, "long", abbrev, team_id, nickname) VALUES ('NASHVILLE', 'NASHVILLE PREDATORS', 'NSH', 18, NULL);
INSERT INTO teams (team, "long", abbrev, team_id, nickname) VALUES ('NEW JERSEY', 'NEW JERSEY DEVILS', 'NJD', 1, NULL);
INSERT INTO teams (team, "long", abbrev, team_id, nickname) VALUES ('NY ISLANDERS', 'NEW YORK ISLANDERS', 'NYI', 2, NULL);
INSERT INTO teams (team, "long", abbrev, team_id, nickname) VALUES ('NY RANGERS', 'NEW YORK RANGERS', 'NYR', 3, NULL);
INSERT INTO teams (team, "long", abbrev, team_id, nickname) VALUES ('OTTAWA', 'OTTAWA SENATORS', 'OTT', 9, NULL);
INSERT INTO teams (team, "long", abbrev, team_id, nickname) VALUES ('PHILADELPHIA', 'PHILADELPHIA FLYERS', 'PHI', 4, NULL);
INSERT INTO teams (team, "long", abbrev, team_id, nickname) VALUES ('PHOENIX', 'PHOENIX COYOTES', 'PHX', 27, NULL);
INSERT INTO teams (team, "long", abbrev, team_id, nickname) VALUES ('PITTSBURGH', 'PITTSBURGH PENGUINS', 'PIT', 5, NULL);
