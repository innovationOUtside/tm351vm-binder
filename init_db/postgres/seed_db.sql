-- Demo PostgreSQL Database initialisation

DROP TABLE IF EXISTS quickdemo CASCADE;
CREATE TABLE quickdemo(id INT, name VARCHAR(20), value INT);
INSERT INTO quickdemo VALUES(1,'This',12);
INSERT INTO quickdemo VALUES(2,'That',345);
