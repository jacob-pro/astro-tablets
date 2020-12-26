/*
* Generate "numbers" / "tally" table of computed years
* (`days` table will always have more rows than the total years)
*/
DROP TABLE IF EXISTS years;
CREATE TEMPORARY TABLE years (
    year INT
);
INSERT INTO years
SELECT ROW_NUMBER() OVER() + (SELECT start_year FROM db_info LIMIT 1) - 1 AS `year`
FROM days LIMIT 1 + (SELECT end_year FROM db_info LIMIT 1) - (SELECT start_year FROM db_info LIMIT 1);
