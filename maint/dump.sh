#!/bin/sh

PSQL=`which psql`
SEASON=20132014

${PSQL} hockey -c "COPY (SELECT * FROM nhl.stats_goalies_special WHERE season = ${SEASON}) TO STDIN WITH CSV HEADER" | gzip > nhl.stats_goalies_special.${SEASON}.csv.gz
${PSQL} hockey -c "COPY (SELECT * FROM nhl.stats_goalies_summary WHERE season = ${SEASON}) TO STDIN WITH CSV HEADER" | gzip > nhl.stats_goalies_summary.${SEASON}.csv.gz

${PSQL} hockey -c "COPY (SELECT * FROM nhl.stats_skaters_summary WHERE season = ${SEASON}) TO STDIN WITH CSV HEADER" | gzip > nhl.stats_skaters_summary.${SEASON}.csv.gz
${PSQL} hockey -c "COPY (SELECT * FROM nhl.stats_skaters_points WHERE season = ${SEASON}) TO STDIN WITH CSV HEADER" | gzip > nhl.stats_skaters_points.${SEASON}.csv.gz
${PSQL} hockey -c "COPY (SELECT * FROM nhl.stats_skaters_faceoff WHERE season = ${SEASON}) TO STDIN WITH CSV HEADER" | gzip > nhl.stats_skaters_faceoff.${SEASON}.csv.gz
${PSQL} hockey -c "COPY (SELECT * FROM nhl.stats_skaters_timeonice WHERE season = ${SEASON}) TO STDIN WITH CSV HEADER" | gzip > nhl.stats_skaters_timeonice.${SEASON}.csv.gz

${PSQL} hockey -c "COPY (SELECT * FROM nhl.games WHERE season = ${SEASON}) TO STDIN WITH CSV HEADER" | gzip > nhl.games.${SEASON}.csv.gz
${PSQL} hockey -c "COPY (SELECT g.* FROM nhl.games_toi g JOIN nhl.games USING (game_id) WHERE season = ${SEASON}) TO STDIN WITH CSV HEADER" | gzip > nhl.games_toi.${SEASON}.csv.gz
${PSQL} hockey -c "COPY (SELECT g.* FROM nhl.games_rosters g JOIN nhl.games USING (game_id) WHERE season = ${SEASON}) TO STDIN WITH CSV HEADER" | gzip > nhl.games_rosters.${SEASON}.csv.gz
${PSQL} hockey -c "COPY (SELECT g.* FROM nhl.games_faceoffs g JOIN nhl.games USING (game_id) WHERE season = ${SEASON}) TO STDIN WITH CSV HEADER" | gzip > nhl.games_faceoffs.${SEASON}.csv.gz

${PSQL} hockey -c "COPY (SELECT g.* FROM nhl.gamelogs_skaters g JOIN nhl.games USING (game_id) WHERE season = ${SEASON}) TO STDIN WITH CSV HEADER" | gzip > nhl.gamelogs_skaters.${SEASON}.csv.gz
${PSQL} hockey -c "COPY (SELECT g.* FROM nhl.gamelogs_goalies g JOIN nhl.games USING (game_id) WHERE season = ${SEASON}) TO STDIN WITH CSV HEADER" | gzip > nhl.gamelogs_goalies.${SEASON}.csv.gz

${PSQL} hockey -c "COPY (SELECT g.* FROM nhl.events g JOIN nhl.games USING (game_id) WHERE season = ${SEASON}) TO STDIN WITH CSV HEADER" | gzip > nhl.events.${SEASON}.csv.gz
${PSQL} hockey -c "COPY (SELECT g.* FROM nhl.events_players g JOIN nhl.games USING (game_id) WHERE season = ${SEASON}) TO STDIN WITH CSV HEADER" | gzip > nhl.events_players.${SEASON}.csv.gz
${PSQL} hockey -c "COPY (SELECT g.* FROM nhl.events_penaltybox g JOIN nhl.games USING (game_id) WHERE season = ${SEASON}) TO STDIN WITH CSV HEADER" | gzip > nhl.events_penaltybox.${SEASON}.csv.gz

${PSQL} hockey -c "COPY (SELECT * FROM nhl.players) TO STDIN WITH CSV HEADER" | gzip > nhl.players.csv.gz
${PSQL} hockey -c "COPY (SELECT * FROM nhl.teams) TO STDIN WITH CSV HEADER" | gzip > nhl.teams.csv.gz

