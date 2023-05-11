-- SQLite
CREATE TABLE flights(
id INTEGER PRIMARY KEY AUTOINCREMENT,
origin TEXT NOT NULL,
destination TEXT NOT NULL,
duration INTEGER NOT NULL);

INSERT INTO flights(origin, destination, duration) VALUES ("New York", "London", 415);

SELECT * FROM flights;

INSERT INTO flights (origin, destination, duration) VALUES ("Shanghai", "Paris", 760);
INSERT INTO flights (origin, destination, duration) VALUES ("Istanbul", "Tokyo", 700);
INSERT INTO flights (origin, destination, duration) VALUES ("New York", "Paris", 435);
INSERT INTO flights (origin, destination, duration) VALUES ("Moscow", "Paris", 245);
INSERT INTO flights (origin, destination, duration) VALUES ("Lima", "New York", 455);


SELECT * FROM flights WHERE origin = "New York";

SELECT * FROM flights WHERE duration > 500;

SELECT * FROM flights WHERE duration > 500 AND destination = "Paris";

SELECT * FROM flights WHERE duration > 500 OR destination = "Paris";

SELECT * FROM flights WHERE origin IN ("New York", "Lima");

SELECT * FROM flights WHERE origin LIKE "%a%";

UPDATE flights SET duration = 430 WHERE origin = "New York" AND destination = "London";

SELECT * FROM flights;

DELETE FROM flights WHERE destination = "Tokyo";

SELECT * FROM flights ORDER BY duration;

SELECT * FROM flights GROUP BY origin;

