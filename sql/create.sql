-- use this file to create tables in predicting-jams database

CREATE TABLE node (
  id BIGINT PRIMARY KEY,
  geometry GEOGRAPHY(POINT, 4326) NOT NULL
);

CREATE TABLE edge (
  node1_id BIGINT,
  node2_id BIGINT,
  distance DOUBLE PRECISION,
  lanes INT2,
  max_velocity DOUBLE PRECISION,
  PRIMARY KEY (node1_id, node2_id),
  FOREIGN KEY (node1_id) REFERENCES node(id),
  FOREIGN KEY (node2_id) REFERENCES node(id)
);

-- TODO: do zastanowienia: może trzeba się też pozbyć tej tabelki jam?
CREATE TABLE jam (
  id BIGINT PRIMARY KEY
);

-- TODO: do zastanowienia: a może skoro jam_removed, jam_20m, jam_40m są takie same, to je złączymy z jakimś dodatkowym polem - enumem?
CREATE TABLE jam_removed (
  jam_id BIGINT,
  event_id BIGINT,
  node1_id BIGINT,
  node2_id BIGINT,
  FOREIGN KEY (jam_id) REFERENCES jam(id),
  FOREIGN KEY (node1_id, node2_id) REFERENCES edge(node1_id, node2_id)
);

CREATE TABLE jam_20m (
  jam_id BIGINT,
  event_id BIGINT,
  node1_id BIGINT,
  node2_id BIGINT,
  FOREIGN KEY (jam_id) REFERENCES jam(id),
  FOREIGN KEY (node1_id, node2_id) REFERENCES edge(node1_id, node2_id)
);

CREATE TABLE jam_40m (
  jam_id BIGINT,
  event_id BIGINT,
  node1_id BIGINT,
  node2_id BIGINT,
  FOREIGN KEY (jam_id) REFERENCES jam(id),
  FOREIGN KEY (node1_id, node2_id) REFERENCES edge(node1_id, node2_id)
);

CREATE TABLE jam_train (
  id BIGINT PRIMARY KEY,
  FOREIGN KEY (id) REFERENCES jam(id)
);

CREATE TABLE jam_test (
  id BIGINT PRIMARY KEY,
  FOREIGN KEY (id) REFERENCES jam(id)
);

CREATE MATERIALIZED VIEW jam_removed_train AS
  SELECT * FROM jam_removed
  WHERE jam_id IN (SELECT id FROM jam_train);

CREATE MATERIALIZED VIEW jam_20m_train AS
  SELECT * FROM jam_20m
  WHERE jam_id IN (SELECT id FROM jam_train);

CREATE MATERIALIZED VIEW jam_40m_train AS
  SELECT * FROM jam_40m
  WHERE jam_id IN (SELECT id FROM jam_train);
