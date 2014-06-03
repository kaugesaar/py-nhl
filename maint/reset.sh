#!/bin/sh

psql hockey -c "drop schema nhl cascade"
psql hockey -c "create schema nhl"
psql hockey -f ../sql/schema.postgresql.sql
psql hockey -f ../sql/lookup.teams.sql
psql hockey -f ../sql/lookup.players_names.sql

