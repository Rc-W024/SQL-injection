CREATE EXTENSION postgis;

CREATE TABLE sim_data (
	id SERIAL PRIMARY KEY,
	username VARCHAR(50),
	password VARCHAR(50) CHECK (char_length(password)>=6),
	geom GEOMETRY(Point,4326) -- WGS 84
);

INSERT INTO sim_data (username,password,geom)
SELECT
	substr(md5(random()::text),1,8) AS username,
	substr(md5(random()::text),1,10) AS password,
	ST_SetSRID(ST_MakePoint(random()*360-180,random()*180-90,4326)) AS geom
FROM generate_series(1,30);