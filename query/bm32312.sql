/* Table of possible year start days, i.e. each year may have 2-3 possible Nisan I dates */
DROP TABLE IF EXISTS potential_years;
CREATE TEMPORARY TABLE potential_years (
    nisan_1 FLOAT,
    year INT
);
INSERT INTO potential_years
SELECT days.sunset as nisan_1, days.year as year
FROM events equinox
INNER JOIN
    days ON days.sunset >= (equinox.time - 31) and days.sunset <= (equinox.time + 31) and days.first_visibility==1
WHERE equinox.event="VernalEquinox" and equinox.body="Sun"
AND days.year <= (SELECT end_year FROM db_info LIMIT 1);

/* Table of possible months in each possible year */
DROP TABLE IF EXISTS potential_months;
CREATE TEMPORARY TABLE potential_months (
    nisan_1 FLOAT,
    year INT,
    sunset FLOAT,
    sunrise FLOAT,
    PRIMARY KEY (nisan_1, sunset)
);
INSERT INTO potential_months
SELECT nisan_1, potential_years.year, days.sunset, days.sunrise
FROM potential_years
INNER JOIN days ON days.first_visibility==1
WHERE days.sunset >= nisan_1
AND days.sunset <= (SELECT MAX(sunset)
FROM (SELECT sunset FROM days WHERE days.first_visibility==1 AND sunset >= nisan_1 ORDER BY sunset LIMIT 12));

/* Insert each month again, but allow starting a day later */
INSERT INTO potential_months
SELECT nisan_1, potential_years.year, days.sunset, days.sunrise
FROM potential_years
INNER JOIN days ON (SELECT first_visibility FROM days as di WHERE di.sunset < days.sunset ORDER BY sunset DESC LIMIT 1) == 1
WHERE days.sunset >= nisan_1
AND days.sunset <= 2 + (SELECT MAX(sunset)
FROM (SELECT sunset FROM days WHERE days.first_visibility==1 AND sunset >= nisan_1 ORDER BY sunset LIMIT 12));

/* Compute results for month A against each possible month in every possible year */
DROP TABLE IF EXISTS month_a_results;
CREATE TEMPORARY TABLE month_a_results (
    nisan_1 FLOAT,
    a_sunset_1 FLOAT,
    year INT,
    MercuryMorningLast14 FLOAT,
    MercuryInPisces14 FLOAT,
    SaturnLastAppearance14 FLOAT,
    SaturnInPisces14 FLOAT,
    MarsStationary17 FLOAT,
    MarsScorpionHead17 FLOAT,
    score INT
);
INSERT INTO month_a_results
SELECT *,
       (CASE WHEN MercuryMorningLast14 IS NOT NULL THEN 1 ELSE 0 END) +
       (CASE WHEN MercuryInPisces14 IS NOT NULL THEN 1 ELSE 0 END) +
       (CASE WHEN SaturnLastAppearance14 IS NOT NULL THEN 1 ELSE 0 END) +
       (CASE WHEN SaturnInPisces14 IS NOT NULL THEN 1 ELSE 0 END) +
       (CASE WHEN MarsStationary17 IS NOT NULL THEN 1 ELSE 0 END) +
       (CASE WHEN MarsScorpionHead17 IS NOT NULL THEN 1 ELSE 0 END) as score
FROM (SELECT nisan_1, sunset as sunset_1, year,
    /* 14th Day ±5 Days */
    (SELECT time FROM events WHERE body="Mercury" AND event="MorningLast"
        AND time >= (sunset + 13 - 5) AND time <= (sunrise + 13 + 5) LIMIT 1) as MercuryMorningLast14,

    /* Between sunset-sunrise of the 14th */
    (SELECT MIN(angle) FROM separations WHERE from_body="Mercury" AND to_body="58 Piscium" AND angle < 50
        AND time >= (SELECT MAX(sunset) FROM (SELECT * FROM days as dz WHERE dz.sunset >= potential_months.sunset ORDER BY dz.sunset LIMIT 14))
        AND time <= (SELECT MAX(sunrise) FROM (SELECT * FROM days as dz WHERE dz.sunset >= potential_months.sunset ORDER BY dz.sunset LIMIT 14))
        LIMIT 1) as MercuryInPisces14,

     /* 14th Day ±10 Days */
    (SELECT time FROM events WHERE body="Saturn" AND event="LastAppearance"
        AND time >= (sunset + 13 - 10) AND time <= (sunrise + 13 + 10) LIMIT 1) as SaturnLastAppearance14,

     /* Between sunset-sunrise of the 14th */
    (SELECT MIN(angle) FROM separations WHERE from_body="Saturn" AND to_body="58 Piscium" AND angle < 50
        AND time >= (SELECT MAX(sunset) FROM (SELECT * FROM days as dz WHERE dz.sunset >= potential_months.sunset ORDER BY dz.sunset LIMIT 14))
        AND time <= (SELECT MAX(sunrise) FROM (SELECT * FROM days as dz WHERE dz.sunset >= potential_months.sunset ORDER BY dz.sunset LIMIT 14))
        LIMIT 1) as SaturnInPisces14,

    /* 14th Day ±20 Days */
    (SELECT time FROM events WHERE body="Mars" AND event="Stationary"
        AND time >= (sunset + 16 - 20) AND time <= (sunrise + 16 + 20) LIMIT 1) as MarsStationary17,

     /* Between sunset-sunrise of the 17th */
    (SELECT MIN(angle) FROM separations WHERE from_body="Mars" AND to_body="Antares" AND angle < 10
        AND time >= (SELECT MAX(sunset) FROM (SELECT * FROM days as dz WHERE dz.sunset >= potential_months.sunset ORDER BY dz.sunset LIMIT 17))
        AND time <= (SELECT MAX(sunrise) FROM (SELECT * FROM days as dz WHERE dz.sunset >= potential_months.sunset ORDER BY dz.sunset LIMIT 17))
        LIMIT 1) as MarsScorpionHead17

    FROM potential_months);

/* Compute results for month B against each possible month in every possible year */
DROP TABLE IF EXISTS month_b_results;
CREATE TEMPORARY TABLE month_b_results (
    nisan_1 FLOAT,
    b_sunset_1 FLOAT,
    year INT,
    MorningFirst5 FLOAT,
    MercuryInPisces5 FLOAT,
    VenusBehindMars19 FLOAT,
    MarsInAries19 FLOAT,
    MarsInAries20 FLOAT,
    score INT
);
INSERT INTO month_b_results
SELECT *,
       (CASE WHEN MorningFirst5 IS NOT NULL THEN 1 ELSE 0 END) +
       (CASE WHEN MercuryInPisces5 IS NOT NULL THEN 1 ELSE 0 END) +
       (CASE WHEN VenusBehindMars19 IS NOT NULL THEN 1 ELSE 0 END) +
       (CASE WHEN MarsInAries19 IS NOT NULL THEN 1 ELSE 0 END) +
       (CASE WHEN MarsInAries20 IS NOT NULL THEN 1 ELSE 0 END) as B_SCORE
FROM (SELECT nisan_1, sunset as sunset_1, year,
     /* 5th Day ±5 Days */
    (SELECT time FROM events WHERE body="Mercury" AND event="MorningFirst"
        AND time >= (sunset + 4 -  5) AND time <= (sunrise + 4 + 5) LIMIT 1) as MorningFirst5,

    /* Between sunset-sunrise of the 5th */
    (SELECT MIN(angle) FROM separations WHERE from_body="Mercury" AND to_body="58 Piscium" AND angle < 50
        AND time >= (SELECT MAX(sunset) FROM (SELECT * FROM days as dz WHERE dz.sunset >= potential_months.sunset ORDER BY dz.sunset LIMIT 5))
        AND time <= (SELECT MAX(sunrise) FROM (SELECT * FROM days as dz WHERE dz.sunset >= potential_months.sunset ORDER BY dz.sunset LIMIT 5))
        LIMIT 1) as MercuryInPisces5,

    /* Between sunset-sunrise of the 19th */
    (SELECT MIN(angle) FROM separations WHERE from_body="Venus" AND to_body="Mars" AND position="behind" AND angle < 5
        AND time >= (SELECT MAX(sunset) FROM (SELECT * FROM days as dz WHERE dz.sunset >= potential_months.sunset ORDER BY dz.sunset LIMIT 19))
        AND time <= (SELECT MAX(sunrise) FROM (SELECT * FROM days as dz WHERE dz.sunset >= potential_months.sunset ORDER BY dz.sunset LIMIT 19))
        LIMIT 1) as VenusBehindMars19,

     /* Between sunset-sunrise of the 19th */
    (SELECT MIN(angle) FROM separations WHERE from_body="Mars" AND to_body="Nu Arietis" AND angle < 30
        AND time >= (SELECT MAX(sunset) FROM (SELECT * FROM days as dz WHERE dz.sunset >= potential_months.sunset ORDER BY dz.sunset LIMIT 19))
        AND time <= (SELECT MAX(sunrise) FROM (SELECT * FROM days as dz WHERE dz.sunset >= potential_months.sunset ORDER BY dz.sunset LIMIT 19))
        LIMIT 1) as MarsInAries19,

     /* Between sunset-sunrise of the 20th */
    (SELECT MIN(angle) FROM separations WHERE from_body="Mars" AND to_body="Nu Arietis" AND angle < 20
        AND time >= (SELECT MAX(sunset) FROM (SELECT * FROM days as dz WHERE dz.sunset >= potential_months.sunset ORDER BY dz.sunset LIMIT 20))
        AND time <= (SELECT MAX(sunrise) FROM (SELECT * FROM days as dz WHERE dz.sunset >= potential_months.sunset ORDER BY dz.sunset LIMIT 20))
        LIMIT 1) as MarsInAries20

    FROM potential_months);

/* Pick best combined results for each year start (i.e. same date for Nisan I)*/
DROP TABLE IF EXISTS joined_results;
CREATE TEMPORARY TABLE joined_results (
    year INT,
    nisan_1 FLOAT,
    a_sunset_1 FLOAT,
    MercuryMorningLast14 FLOAT,
    MercuryInPisces14 FLOAT,
    SaturnLastAppearance14 FLOAT,
    SaturnInPisces14 FLOAT,
    MarsStationary17 FLOAT,
    MarsScorpionHead17 FLOAT,
    b_sunset_1 FLOAT,
    MorningFirst5 FLOAT,
    MercuryInPisces5 FLOAT,
    VenusBehindMars19 FLOAT,
    MarsInAries19 FLOAT,
    MarsInAries20 FLOAT,
    total_score INT
);
INSERT INTO joined_results
SELECT a_results.year, a_results.nisan_1, a_sunset_1,
       MercuryMorningLast14, MercuryInPisces14, SaturnLastAppearance14, SaturnInPisces14, MarsStationary17, MarsScorpionHead17,
       b_sunset_1, MorningFirst5, MercuryInPisces5, VenusBehindMars19, MarsInAries19, MarsInAries20,
       a_results.score + b_results.score as total_score FROM
(SELECT * FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY nisan_1 ORDER BY score DESC) as position
    FROM month_a_results)
WHERE position <= 1) as a_results
INNER JOIN
(SELECT * FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY nisan_1 ORDER BY score DESC) as position
    FROM month_b_results)
WHERE position <= 1) as b_results
ON a_results.nisan_1 = b_results.nisan_1;

/* Pick best results for each year number */
SELECT * FROM joined_results o
WHERE o.total_score = (
    SELECT MAX(total_score) FROM joined_results x WHERE x.year=o.year LIMIT 1
)
ORDER BY total_score DESC;
