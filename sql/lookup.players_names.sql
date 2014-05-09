/*
*
* These are alternative player names used by NHL.com (different than the ones
* stored in the players table). This is populated on a random basis as I find them.
* mysql users: remove the SET call
*
*/

SET search_path to nhl;

DROP TABLE IF EXISTS players_names;

CREATE TABLE players_names (
    player_id integer references nhl.players(player_id),
    player_name varchar(255),
    primary key (player_id, player_name)
);

INSERT INTO players_names VALUES
    (8464975, 'DANNY BRIERE'),
    (8466149, 'DANNY CLEARY'),
    (8466149, 'DAN CLEARY'),
    (8469500, 'MICHAEL CAMMALLERI'),
    (8471269, 'NICKLAS GROSSMAN'), -- Just a mispelling w/o the extra n!
    (8467899, 'MARTIN HAVLAT'),
    (8475739, 'MICHAEL BOURNIVAL'),
    (8467428, 'KRYS BARCH'),
    (8460556, 'FREDRIK MODIN'),
    (8471413, 'MICHAEL VERNACE'),
    (8471508, 'OLIVIER MAGNAN-GRENIER'),
    (8468432, 'STEVEN REINPRECHT'),
    (8470647, 'BJ CROMBEEN'),
    (8467336, 'MICHAEL RUPP'),
    (8471698, 'TJ OSHIE'),
    (8470666, 'DAN CARCILLO'),
    (8474149, 'EVGENY DADONOV'),
    (8474591, 'THOMAS MCCOLLUM'),
    (8471753, 'TJ HENSICK'),
    (8471762, 'CHRIS VANDE VELDE'),
    (8471832, 'NICHOLAS DRAZENOVIC'),
    (8473927, 'BRADLEY MILLS'),
    (8470366, 'MARTIN ST PIERRE'),
    (8476856, 'MATT DUMBA'),
    (8466378, 'MARTIN ST LOUIS'),
    (8466378, 'MARTIN ST. LOUIS'),
    (8476856, 'MATHEW DUMBA'),
    (8470640, 'MATT CARLE'),
    (8470640, 'MATTHEW, CARLE'),
    (8470640, 'CARLE, MATTHEW'),
    (8470640, 'MATTHEW CARLE'),
    (8469500, 'MIKE CAMMALLERI'),
    (8470647, 'B.J. CROMBEEN'),
    (8477227, 'ERIAH HAYES'),
    (8464975, 'DANIEL BRIERE'),
    (8471269, 'NICKLAS GROSSMANN'),
    (8471762, 'CHRIS VANDEVELDE'),
    (8471698, 'T.J. OSHIE'),
    (8474596, 'JAKE ALLEN'),
    (8467336, 'MIKE RUPP'),
    (8470666, 'DANIEL CARCILLO'),
    (8471214, 'ALEX OVECHKIN'),
    (8466149, 'DANIEL CLEARY'),
    (8474754, 'JOACIM ERIKSSON'),
    (8467899, 'MARTY HAVLAT'),
    (8477244, 'CHAD RUHWEDEL'),
    (8476442, 'MATTHEW NIETO'),
    (8476442, 'MATT NIETO'),
    (8474729, 'MIKE MURPHY'),
    (8474688, 'GREG PATERYN'),
    (8473927, 'BRAD MILLS'),
    (8475739, 'MICHAËL BOURNIVAL'),
    (8477811, 'RYAN HAGGERTY'),
    (8477092, 'ANDREY MAKAROV'),
    (8476373, 'NIKLAS LUNDSTROM'),
    (8477715, 'TYLER GAUDET'),
    (8475241, 'SERGEY ANDRONOV');