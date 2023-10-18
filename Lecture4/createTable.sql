CREATE TABLE flights(
    id INTEGER PRIMARY KEY IDENTITY,
    origin TEXT NOT NULL,
    destination TEXT NOT NULL,
    duration INTEGER NOT NULL
);
/* integer/text defines the column type
PRIMARY KEY states that it will be the primary sorting mechanism
NOT NULL means that you cannot have a null entry
AUTOINCREMENT/IDENTITY means that it will automatically increment*/

INSERT INTO flights
    (origin, destination, duration)
    VALUES ("New York", "London", 415)
/* inserts one row into the table flights */

SELECT * FROM flights;
/* shows every row and column in the table */

SELECT * FROM flights WHERE origin = "New York";

SELECT * FROM flights WHERE duration > 50 AND destination = "Paris";
SELECT * FROM flights WHERE duration > 50 OR destination = "Paris";
/* can use AND/OR to use multiple conditions */

SELECT * FROM flights WHERE origin IN ("New York", "Lima");

/* wild card --> looks for all entries that have an "a" in the origin */
SELECT * FROM flights WHERE origin LIKE "%a%";

/* finds all rows where origin is New York and destination
is Paris and updates the duration to be 430 */
UPDATE flights
    SET duration = 430
    WHERE origin = "New York"
    AND destination = "London";

/* delete statement self-explanatory */
DELETE FROM flights WHERE destination = "Tokyo";

/* to join multiple tables... */
SELECT first, origin, destination
FROM flights JOIN passengers
ON passengers.flight_id = flights.id;
/* joins on flight's id column to passenger's flight_id column */


/* create an index based on a passenger's last name
to all for easy value look up */
CREATE INDEX name_index ON passengers (last);