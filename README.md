# Predicting traffic jams [![Build Status](https://travis-ci.org/jedrz/predicting-jams.svg)](https://travis-ci.org/jedrz/predicting-jams) [![Sputnik](https://sputnik.ci/conf/badge)](https://sputnik.ci/app#/builds/jedrz/predicting-jams) [![codecov](https://codecov.io/gh/jedrz/predicting-jams/branch/master/graph/badge.svg)](https://codecov.io/gh/jedrz/predicting-jams)

## Data sets

Data sets are downloaded from http://tunedit.org/challenge/IEEE-ICDM-2010/jams.

## Database

We are using docker image with postgresql and postgis extension from https://hub.docker.com/r/kartoza/postgis/.
To run container:
```bash
sudo docker run --name "postgis" -p 25432:5432 -d -t kartoza/postgis
```
Then to connect to database using psql:
```bash
psql -h localhost -U docker -p 25432 -d postgres
```
and then:
```bash
create database "predicting-jams" owner docker encoding 'UTF8' template template_postgis;
```
To create schema connect to *predicting-jams* using psql from project root directory and then type:
```bash
\i sql/create.sql 
```
To drop schema:
```bash
\i sql/drop.sql 
```
