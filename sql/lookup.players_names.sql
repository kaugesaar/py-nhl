/*
*
* These are alternative player names used by NHL.com (different than the ones
* stored in the players table). This is populated on a random basis as I find them.
*
*/

SET search_path to nhl;

DROP TABLE IF EXISTS players_names;

CREATE TABLE players_names (
    player_id integer references nhl.players(player_id),
    player_name text,
    primary key (player_id, player_name)
);

INSERT INTO players_names VALUES
    (8464975, 'DANNY BRIERE'),
    (8466149, 'DANNY CLEARY'),
    (8469500, 'MICHAEL CAMMALLERI'),
    (8471269, 'NICKLAS GROSSMAN'), -- Just a mispelling w/o the extra n!
    (8467899, 'MARTIN HAVLAT'),
    (8475739, 'MICHAEL BOURNIVAL'),
    (8467428, 'KRYS BARCH'),
    (8470640, 'MATT CARLE');
