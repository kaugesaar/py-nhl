SET search_path to nhl;

TRUNCATE alignment;

-- 2005/2006 - 2010/2011

CREATE TEMPORARY TABLE _years (year INTEGER);

INSERT INTO _years VALUES(2005), (2006), (2007), (2008), (2009), (2010);

INSERT INTO alignment SELECT (year::text||year+1)::integer, 'NEW JERSEY', 'ATLANTIC', 'EASTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'PHILADELPHIA', 'ATLANTIC', 'EASTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'NY RANGERS', 'ATLANTIC', 'EASTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'NY ISLANDERS', 'ATLANTIC', 'EASTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'PITTSBURGH', 'ATLANTIC', 'EASTERN' FROM _years;

INSERT INTO alignment SELECT (year::text||year+1)::integer, 'OTTAWA', 'NORTHEAST', 'EASTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'BUFFALO', 'NORTHEAST', 'EASTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'MONTREAL', 'NORTHEAST', 'EASTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'TORONTO', 'NORTHEAST', 'EASTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'BOSTON', 'NORTHEAST', 'EASTERN' FROM _years;

INSERT INTO alignment SELECT (year::text||year+1)::integer, 'CAROLINA', 'SOUTHEAST', 'EASTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'TAMPA BAY', 'SOUTHEAST', 'EASTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'ATLANTA', 'SOUTHEAST', 'EASTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'FLORIDA', 'SOUTHEAST', 'EASTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'WASHINGTON', 'SOUTHEAST', 'EASTERN' FROM _years;

INSERT INTO alignment SELECT (year::text||year+1)::integer, 'DETROIT', 'CENTRAL', 'WESTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'NASHVILLE', 'CENTRAL', 'WESTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'COLUMBUS', 'CENTRAL', 'WESTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'CHICAGO', 'CENTRAL', 'WESTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'ST LOUIS', 'CENTRAL', 'WESTERN' FROM _years;

INSERT INTO alignment SELECT (year::text||year+1)::integer, 'CALGARY', 'NORTHWEST', 'WESTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'COLORADO', 'NORTHWEST', 'WESTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'EDMONTON', 'NORTHWEST', 'WESTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'VANCOUVER', 'NORTHWEST', 'WESTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'MINNESOTA', 'NORTHWEST', 'WESTERN' FROM _years;

INSERT INTO alignment SELECT (year::text||year+1)::integer, 'DALLAS', 'PACIFIC', 'WESTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'SAN JOSE', 'PACIFIC', 'WESTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'ANAHEIM', 'PACIFIC', 'WESTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'LOS ANGELES', 'PACIFIC', 'WESTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'PHOENIX', 'PACIFIC', 'WESTERN' FROM _years;

-- 2011/2012 - 2012/2013

TRUNCATE _years;

INSERT INTO _years VALUES(2011), (2012);

INSERT INTO alignment SELECT (year::text||year+1)::integer, 'NEW JERSEY', 'ATLANTIC', 'EASTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'PHILADELPHIA', 'ATLANTIC', 'EASTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'NY RANGERS', 'ATLANTIC', 'EASTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'NY ISLANDERS', 'ATLANTIC', 'EASTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'PITTSBURGH', 'ATLANTIC', 'EASTERN' FROM _years;

INSERT INTO alignment SELECT (year::text||year+1)::integer, 'OTTAWA', 'NORTHEAST', 'EASTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'BUFFALO', 'NORTHEAST', 'EASTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'MONTREAL', 'NORTHEAST', 'EASTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'TORONTO', 'NORTHEAST', 'EASTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'BOSTON', 'NORTHEAST', 'EASTERN' FROM _years;

INSERT INTO alignment SELECT (year::text||year+1)::integer, 'CAROLINA', 'SOUTHEAST', 'EASTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'TAMPA BAY', 'SOUTHEAST', 'EASTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'WINNIPEG', 'SOUTHEAST', 'WESTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'FLORIDA', 'SOUTHEAST', 'EASTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'WASHINGTON', 'SOUTHEAST', 'EASTERN' FROM _years;

INSERT INTO alignment SELECT (year::text||year+1)::integer, 'DETROIT', 'CENTRAL', 'WESTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'NASHVILLE', 'CENTRAL', 'WESTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'COLUMBUS', 'CENTRAL', 'WESTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'CHICAGO', 'CENTRAL', 'WESTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'ST LOUIS', 'CENTRAL', 'WESTERN' FROM _years;

INSERT INTO alignment SELECT (year::text||year+1)::integer, 'CALGARY', 'NORTHWEST', 'WESTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'COLORADO', 'NORTHWEST', 'WESTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'EDMONTON', 'NORTHWEST', 'WESTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'VANCOUVER', 'NORTHWEST', 'WESTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'MINNESOTA', 'NORTHWEST', 'WESTERN' FROM _years;

INSERT INTO alignment SELECT (year::text||year+1)::integer, 'DALLAS', 'PACIFIC', 'WESTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'SAN JOSE', 'PACIFIC', 'WESTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'ANAHEIM', 'PACIFIC', 'WESTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'LOS ANGELES', 'PACIFIC', 'WESTERN' FROM _years;
INSERT INTO alignment SELECT (year::text||year+1)::integer, 'PHOENIX', 'PACIFIC', 'WESTERN' FROM _years;

-- 2013/2014 - present

INSERT INTO alignment VALUES(20132014, 'BOSTON', 'ATLANTIC', 'EASTERN');
INSERT INTO alignment VALUES(20132014, 'TAMPA BAY', 'ATLANTIC', 'EASTERN');
INSERT INTO alignment VALUES(20132014, 'MONTREAL', 'ATLANTIC', 'EASTERN');
INSERT INTO alignment VALUES(20132014, 'DETROIT', 'ATLANTIC', 'EASTERN');
INSERT INTO alignment VALUES(20132014, 'OTTAWA', 'ATLANTIC', 'EASTERN');
INSERT INTO alignment VALUES(20132014, 'TORONTO', 'ATLANTIC', 'EASTERN');
INSERT INTO alignment VALUES(20132014, 'FLORIDA', 'ATLANTIC', 'EASTERN');
INSERT INTO alignment VALUES(20132014, 'BUFFALO', 'ATLANTIC', 'EASTERN');

INSERT INTO alignment VALUES(20132014, 'PITTSBURGH', 'METROPOLITAN', 'EASTERN');
INSERT INTO alignment VALUES(20132014, 'NY RANGERS', 'METROPOLITAN', 'EASTERN');
INSERT INTO alignment VALUES(20132014, 'PHILADELPHIA', 'METROPOLITAN', 'EASTERN');
INSERT INTO alignment VALUES(20132014, 'COLUMBUS', 'METROPOLITAN', 'EASTERN');
INSERT INTO alignment VALUES(20132014, 'WASHINGTON', 'METROPOLITAN', 'EASTERN');
INSERT INTO alignment VALUES(20132014, 'NEW JERSEY', 'METROPOLITAN', 'EASTERN');
INSERT INTO alignment VALUES(20132014, 'CAROLINA', 'METROPOLITAN', 'EASTERN');
INSERT INTO alignment VALUES(20132014, 'NY ISLANDERS', 'METROPOLITAN', 'EASTERN');

INSERT INTO alignment VALUES(20132014, 'COLORADO', 'CENTRAL', 'WESTERN');
INSERT INTO alignment VALUES(20132014, 'ST LOUIS', 'CENTRAL', 'WESTERN');
INSERT INTO alignment VALUES(20132014, 'CHICAGO', 'CENTRAL', 'WESTERN');
INSERT INTO alignment VALUES(20132014, 'MINNESOTA', 'CENTRAL', 'WESTERN');
INSERT INTO alignment VALUES(20132014, 'DALLAS', 'CENTRAL', 'WESTERN');
INSERT INTO alignment VALUES(20132014, 'NASHVILLE', 'CENTRAL', 'WESTERN');
INSERT INTO alignment VALUES(20132014, 'WINNIPEG', 'CENTRAL', 'WESTERN');

INSERT INTO alignment VALUES(20132014, 'ANAHEIM', 'PACIFIC', 'WESTERN');
INSERT INTO alignment VALUES(20132014, 'SAN JOSE', 'PACIFIC', 'WESTERN');
INSERT INTO alignment VALUES(20132014, 'LOS ANGELES', 'PACIFIC', 'WESTERN');
INSERT INTO alignment VALUES(20132014, 'PHOENIX', 'PACIFIC', 'WESTERN');
INSERT INTO alignment VALUES(20132014, 'VANCOUVER', 'PACIFIC', 'WESTERN');
INSERT INTO alignment VALUES(20132014, 'CALGARY', 'PACIFIC', 'WESTERN');
INSERT INTO alignment VALUES(20132014, 'EDMONTON', 'PACIFIC', 'WESTERN');