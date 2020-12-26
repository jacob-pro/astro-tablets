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
    sunset FLOAT
);
INSERT INTO potential_months
SELECT nisan_1, potential_years.year, days.sunset
FROM potential_years
INNER JOIN days ON days.first_visibility==1
WHERE days.sunset >= nisan_1
AND days.sunset <= (SELECT MAX(sunset)
FROM (SELECT sunset FROM days WHERE days.first_visibility==1 AND sunset >= nisan_1 ORDER BY sunset LIMIT 12));

SELECT * FROM potential_months

