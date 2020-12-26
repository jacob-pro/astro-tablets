/* Table of possible year start days */
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
    sunrise FLOAT
);
INSERT INTO potential_months
SELECT nisan_1, potential_years.year, days.sunset, days.sunrise
FROM potential_years
INNER JOIN days ON days.first_visibility==1
WHERE days.sunset >= nisan_1
AND days.sunset <= (SELECT MAX(sunset)
FROM (SELECT sunset FROM days WHERE days.first_visibility==1 AND sunset >= nisan_1 ORDER BY sunset LIMIT 12));

SELECT *,
       (CASE WHEN MercuryMorningLast14 IS NOT NULL THEN 1 ELSE 0 END) +
       (CASE WHEN MercuryInPisces14 IS NOT NULL THEN 1 ELSE 0 END) +
       (CASE WHEN SaturnLastAppearance14 IS NOT NULL THEN 1 ELSE 0 END) +
       (CASE WHEN SaturnInPisces14 IS NOT NULL THEN 1 ELSE 0 END) +
       (CASE WHEN MarsStationary17 IS NOT NULL THEN 1 ELSE 0 END) +
       (CASE WHEN MarsScorpionHead17 IS NOT NULL THEN 1 ELSE 0 END) as SCORE
FROM (SELECT sunset, year,
    (SELECT time FROM events WHERE body="Mercury" AND event="MorningLast"
        AND time >= (sunset + 13 -  5) AND time <= (sunrise + 13 + 5) LIMIT 1) as MercuryMorningLast14,
    (SELECT MIN(angle) FROM separations WHERE from_body="Mercury" AND to_body="58 Piscium"
        AND angle < 50 AND time >= (sunset + 13) AND time <= (sunrise + 13) LIMIT 1) as MercuryInPisces14,
    (SELECT time FROM events WHERE body="Saturn" AND event="LastAppearance"
        AND time >= (sunset + 13 - 5) AND time <= (sunrise + 13 + 5) LIMIT 1) as SaturnLastAppearance14,
    (SELECT MIN(angle) FROM separations WHERE from_body="Saturn" AND to_body="58 Piscium"
        AND angle < 50 AND time >= (sunset + 13) AND time <= (sunrise + 13) LIMIT 1) as SaturnInPisces14,
    (SELECT time FROM events WHERE body="Mars" AND event="Stationary"
        AND time >= (sunset + 16 - 20) AND time <= (sunrise + 16 + 20) LIMIT 1) as MarsStationary17,
    (SELECT MIN(angle) FROM separations WHERE from_body="Mars" AND to_body="Antares"
        AND angle < 10 AND time >= (sunset + 16) AND time <= (sunrise + 16) LIMIT 1) as MarsScorpionHead17
    FROM potential_months)
ORDER BY SCORE DESC;

