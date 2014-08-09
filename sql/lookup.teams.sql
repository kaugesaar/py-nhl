/*
*
* Contains all NHL teams as they appear in various reports
* mysql users: remove the SET call (or hey, switch to postgres!)
*
*/

SET search_path to nhl;

DELETE FROM teams;

INSERT INTO teams (team, longname, abbrev, team_id, play_abbrev) VALUES ('TAMPA BAY', 'TAMPA BAY LIGHTNING', 'TBL', 14, 'T.B');
INSERT INTO teams (team, longname, abbrev, team_id, play_abbrev) VALUES ('SAN JOSE', 'SAN JOSE SHARKS', 'SJS', 28, 'S.J');
INSERT INTO teams (team, longname, abbrev, team_id, play_abbrev) VALUES ('MONTREAL', 'MONTREAL CANADIENS', 'MTL', 8, 'MTL');
INSERT INTO teams (team, longname, abbrev, team_id, play_abbrev) VALUES ('ST LOUIS', 'ST. LOUIS BLUES', 'STL', 19, 'STL');
INSERT INTO teams (team, longname, abbrev, team_id, play_abbrev) VALUES ('TORONTO', 'TORONTO MAPLE LEAFS', 'TOR', 10, 'TOR');
INSERT INTO teams (team, longname, abbrev, team_id, play_abbrev) VALUES ('VANCOUVER', 'VANCOUVER CANUCKS', 'VAN', 23, 'VAN');
INSERT INTO teams (team, longname, abbrev, team_id, play_abbrev) VALUES ('WASHINGTON', 'WASHINGTON CAPITALS', 'WSH', 15, 'WSH');
INSERT INTO teams (team, longname, abbrev, team_id, play_abbrev) VALUES ('WINNIPEG', 'WINNIPEG JETS', 'WPG', 52, 'WPG');
INSERT INTO teams (team, longname, abbrev, team_id, play_abbrev) VALUES ('ATLANTA', 'ATLANTA THRASHERS', 'ATL', NULL, 'ATL');
INSERT INTO teams (team, longname, abbrev, team_id, play_abbrev) VALUES ('ANAHEIM', 'ANAHEIM DUCKS', 'ANA', 24, 'ANA');
INSERT INTO teams (team, longname, abbrev, team_id, play_abbrev) VALUES ('BOSTON', 'BOSTON BRUINS', 'BOS', 6, 'BOS');
INSERT INTO teams (team, longname, abbrev, team_id, play_abbrev) VALUES ('BUFFALO', 'BUFFALO SABRES', 'BUF', 7, 'BUF');
INSERT INTO teams (team, longname, abbrev, team_id, play_abbrev) VALUES ('CALGARY', 'CALGARY FLAMES', 'CGY', 20, 'CGY');
INSERT INTO teams (team, longname, abbrev, team_id, play_abbrev) VALUES ('CAROLINA', 'CAROLINA HURRICANES', 'CAR', 12, 'CAR');
INSERT INTO teams (team, longname, abbrev, team_id, play_abbrev) VALUES ('CHICAGO', 'CHICAGO BLACKHAWKS', 'CHI', 16, 'CHI');
INSERT INTO teams (team, longname, abbrev, team_id, play_abbrev) VALUES ('COLORADO', 'COLORADO AVALANCHE', 'COL', 21, 'COL');
INSERT INTO teams (team, longname, abbrev, team_id, play_abbrev) VALUES ('COLUMBUS', 'COLUMBUS BLUE JACKETS', 'CBJ', 29, 'CBJ');
INSERT INTO teams (team, longname, abbrev, team_id, play_abbrev) VALUES ('DALLAS', 'DALLAS STARS', 'DAL', 25, 'DAL');
INSERT INTO teams (team, longname, abbrev, team_id, play_abbrev) VALUES ('DETROIT', 'DETROIT RED WINGS', 'DET', 17, 'DET');
INSERT INTO teams (team, longname, abbrev, team_id, play_abbrev) VALUES ('EDMONTON', 'EDMONTON OILERS', 'EDM', 22, 'EDM');
INSERT INTO teams (team, longname, abbrev, team_id, play_abbrev) VALUES ('FLORIDA', 'FLORIDA PANTHERS', 'FLA', 13, 'FLA');
INSERT INTO teams (team, longname, abbrev, team_id, play_abbrev) VALUES ('MINNESOTA', 'MINNESOTA WILD', 'MIN', 30, 'MIN');
INSERT INTO teams (team, longname, abbrev, team_id, play_abbrev) VALUES ('NASHVILLE', 'NASHVILLE PREDATORS', 'NSH', 18, 'NSH');
INSERT INTO teams (team, longname, abbrev, team_id, play_abbrev) VALUES ('NY ISLANDERS', 'NEW YORK ISLANDERS', 'NYI', 2, 'NYI');
INSERT INTO teams (team, longname, abbrev, team_id, play_abbrev) VALUES ('NY RANGERS', 'NEW YORK RANGERS', 'NYR', 3, 'NYR');
INSERT INTO teams (team, longname, abbrev, team_id, play_abbrev) VALUES ('OTTAWA', 'OTTAWA SENATORS', 'OTT', 9, 'OTT');
INSERT INTO teams (team, longname, abbrev, team_id, play_abbrev) VALUES ('PHILADELPHIA', 'PHILADELPHIA FLYERS', 'PHI', 4, 'PHI');
INSERT INTO teams (team, longname, abbrev, team_id, play_abbrev) VALUES ('PHOENIX', 'PHOENIX COYOTES', 'PHX', 27, 'PHX');
INSERT INTO teams (team, longname, abbrev, team_id, play_abbrev) VALUES ('PITTSBURGH', 'PITTSBURGH PENGUINS', 'PIT', 5, 'PIT');
INSERT INTO teams (team, longname, abbrev, team_id, play_abbrev) VALUES ('ARIZONA', 'ARIZONA COYOTES', 'ARI', NULL, 'ARI');
INSERT INTO teams (team, longname, abbrev, team_id, play_abbrev) VALUES ('LOS ANGELES', 'LOS ANGELES KINGS', 'LAK', 26, 'L.A');
INSERT INTO teams (team, longname, abbrev, team_id, play_abbrev) VALUES ('NEW JERSEY', 'NEW JERSEY DEVILS', 'NJD', 1, 'N.J');