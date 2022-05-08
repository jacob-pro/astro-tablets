# User Guide

## Overview

The majority of texts supported by this program have already been dated by AJ Sachs and H Hunger in the
*Astronomical Diaries and Related Texts From Babylonia* (ADT) series. How did they do it?

> DATING THE DIARIES <br />
  Very few diaries have been preserved intact. When the statement of date is broken
  away, how does one proceed in an effort to establish the date?  <br />
  A dense network of positions for the planets, sun, and moon during the last six
  centuries B.C. is available in Tuckerman. Using the tables of C. Schoch and P.V.
  Neugebauer, A. Sachs computed for the period from -450 to -10 the planetary phenomena
  which the Babylonians considered significant: last appearance, first appearance,
  stationary points and (for outer planets) acronychal rising. Tables for lunar and solar
  eclipses exist; I mention P. V. Neugebauer, Spezieller Kanon der Mondfinsternisse ....,
  Astronomische Abhandlungen 9/2 (1934) and Spezieller Kanon der Sonnenfinsternisse
  ...., Astronomische Abhandlungen 8/4 (1931), and the recent work by H. Mucke and J.
  Meeus, Canon of Solar Eclipses, and Canon of Lunar Eclipses (Vienna 1983). For the last
  several centuries B.C., the Babylonian scheme for the dates of solstices, equinoxes, and
  Sirius phenomena is known and can help to determine the date of a diary. <br />
  It is, of course, trivial that the mention of a king Arsaces means that there is no need
  to look for a date before SE 170. The occurrence of the city Seleucia makes only dates
  beginning with the 3rd century B.C. possible. Less trivial criteria, like changes in orthographic
  conventions, emerge after one arranges the already dated texts in their chronological
  sequence. [@sachs1988adt, 19]

The *astro-tablets* program takes a similar approach of testing the diaries against tables of relevant
astronomical data, however it has the aim of being less reliant on
external chronological information and assumptions. 
To do, so it works by testing a text against astronomical tables for a given base year completely automatically,
and then repeating this in a brute force fashion across a large range of possible years.

Using *astro-tablets* requires two stages, in the 'generate' stage, a database is created containing
all the necessary astronomical data for the observations in a text, 
using the [Skyfield](https://rhodesmill.org/skyfield/) astronomy library.

In the 'query' stage, the database is then repeatedly tested with different base years,
and a total score is computed, allowing the base years to be ranked for the best match.

## Installation

### Using Docker

```bash
docker run --rm -it \
  -v ${PWD}/generated:/astro-tablets/generated \
  -v ${PWD}/skyfield-data:/astro-tablets/skyfield-data \
  ghcr.io/jacob-pro/astro-tablets:latest \
  --help
```

### Manually

1. Ensure you have *Python* 3.7+ and *Make* installed.
2. Run `make venv/requirements`.
3. Run `venv/bin/activate` (or equivalent)
4. Run `python ./src/main.py --help`.

## The Generate Stage

To create the database for a given tablet use the `generate` subcommand:

```
$ python ./src/main.py generate --help 
usage: main.py generate [-h] [--db DB] [--overwrite] [--start START] [--end END] {BM32312,BM41222,BM76738,BM35115,BM32234,BM38462,VAT4956,BM33066}

positional arguments:
  {BM32312,BM41222,BM76738,BM35115,BM32234,BM38462,VAT4956,BM33066}
                        name of the tablet to generate ephemeris for

optional arguments:
  -h, --help            show this help message and exit
  --db DB               override path to save the database to
  --overwrite           overwrite the database if exists
  --start START         override start year
  --end END             override end year

```

By default, the database will be saved to `./generated/${TABLET}.db`. If the file already exists
it will prompt before overwriting, unless the `--overwrite` option is set.

Each tablet has a default start and end year associated with it, roughly 100 years around its expected
dating, this can be overridden with the `--start` and `--end` flags.

The generate stage can take a very long time (e.g. 10 hours) and produce a large database file (e.g. 300MB),
depending on the complexity of the tablet, and the number of years being generated.

The generated database is in *SQLite* format and stores tables with all the necessary event times and ephemeris,
for example:

![](img/events_table_example.png)

## The Query Stage

Once a database has been generated for a tablet, then the `query_all` and  `query_year` subcommands can be run:

```
$ python ./src/main.py query_all --help
usage: main.py query_all [-h] [--db DB] [--output OUTPUT] {BM32312,BM41222,BM76738,BM35115,BM32234,BM38462,VAT4956,BM33066} [subquery]

positional arguments:
  {BM32312,BM41222,BM76738,BM35115,BM32234,BM38462,VAT4956,BM33066}
                        name of the tablet to query ephemeris for
  subquery              Optional subquery

optional arguments:
  -h, --help            show this help message and exit
  --db DB               override path to source database
  --output OUTPUT       override path to save output
```

The tablet names are the same as in the previous stage, by default it will look for the database at
`./generated/${TABLET}.db` (although this can be overridden with the `--db` flag).

`query_all` will run the tests against all the years that the database file contains, and then output a text file
containing the scores for each.

To get a report for a specific base year use the `query_year` subcommand; it will produce a JSON file containing 
all the details of the matched observations:

```
$ python ./src/main.py query_year --help
usage: main.py query_year [-h] [--db DB] [--output OUTPUT] [--full] {BM32312,BM41222,BM76738,BM35115,BM32234,BM38462,VAT4956,BM33066} year [subquery]

positional arguments:
  {BM32312,BM41222,BM76738,BM35115,BM32234,BM38462,VAT4956,BM33066}
                        name of the tablet to query ephemeris for
  year                  the base year to query
  subquery              Optional subquery

optional arguments:
  -h, --help            show this help message and exit
  --db DB               override path to source database
  --output OUTPUT       override path to save output
  --full                output all possible year start combinations
```

Use the `--full` option to show all the possible year start dates (a year can in theory begin at any of the first lunar 
visibilities close to the vernal equinox. 
When the intercalary month information is known then the compatibility of adjacent year start dates can be assessed.
The compatible sequence of years with the highest score (as used in the main result) will be flagged with 
`best_compatible_path` field. 

## Other Commands

To regenerate the graphs found in `./documents/graphics` use this command:

```
python ./src/main.py graphs ./documents/graphics
```

## Testing

```
make test
```

The unit tests check that the astronomical computation functions are working correctly by comparing the results with 
data from other sources (commercial software, and academic publications).

## References
