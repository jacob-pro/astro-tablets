User Guide
==========

Overview
--------

The majority of texts supported by this program have already been dated
by AJ Sachs and H Hunger in the *Astronomical Diaries and Related Texts
From Babylonia* (ADT) series. How did they do it?

> DATING THE DIARIES <br /> Very few diaries have been preserved intact.
> When the statement of date is broken away, how does one proceed in an
> effort to establish the date? <br /> A dense network of positions for
> the planets, sun, and moon during the last six centuries B.C. is
> available in Tuckerman. Using the tables of C. Schoch and P.V.
> Neugebauer, A. Sachs computed for the period from -450 to -10 the
> planetary phenomena which the Babylonians considered significant: last
> appearance, first appearance, stationary points and (for outer
> planets) acronychal rising. Tables for lunar and solar eclipses exist;
> I mention P. V. Neugebauer, Spezieller Kanon der Mondfinsternisse ….,
> Astronomische Abhandlungen 9/2 (1934) and Spezieller Kanon der
> Sonnenfinsternisse …., Astronomische Abhandlungen 8/4 (1931), and the
> recent work by H. Mucke and J. Meeus, Canon of Solar Eclipses, and
> Canon of Lunar Eclipses (Vienna 1983). For the last several centuries
> B.C., the Babylonian scheme for the dates of solstices, equinoxes, and
> Sirius phenomena is known and can help to determine the date of a
> diary. <br /> It is, of course, trivial that the mention of a king
> Arsaces means that there is no need to look for a date before SE 170.
> The occurrence of the city Seleucia makes only dates beginning with
> the 3rd century B.C. possible. Less trivial criteria, like changes in
> orthographic conventions, emerge after one arranges the already dated
> texts in their chronological sequence. \[1, p. 19\]

The *astro-tablets* program takes a similar approach of testing the
diaries against tables of relevant astronomical data, however it has the
aim of being less reliant on external chronological information and
assumptions. To do, so it works by testing a text against astronomical
tables for a given base year completely automatically, and then
repeating this in a brute force fashion across a large range of possible
years.

Running *astro-tablets* requires two stages, in the first stage
`generate`, a database is created containing all the necessary
astronomical data for the observations in a text, using the
[Skyfield](https://rhodesmill.org/skyfield/) astronomy library. In the
second stage `query`, that database is then repeatedly queried with
different base years, and a total score is computed, allowing the base
years to be ranked for the best match.

Installation
------------

### Using Docker

    git clone https://github.com/jacob-pro/astro-tablets.git
    cd astro-tablets
    docker build -t astro-tablets .
    docker run --rm -it -v ${PWD}/generated:/astro-tablets/generated -v ${PWD}/skyfield-data:/astro-tablets/skyfield-data \
    astro-tablets *SUBCOMMAND* *ARGS*

### Manually

1.  Requires Python 3.7
2.  Install `requirements.txt` using Pip
3.  If using an IDE like PyCharm define `./src` as a source folder in
    project structure
4.  Run `python ./src/main.py *SUBCOMMAND* *ARGS*`

The Generate Stage
------------------

The Query Stage
---------------

References
----------

\[1\] H. Hunger and A. J. Sachs, *Astronomical diaries and related texts
from Babylonia. Vol. 1, Diaries from 652 B.C. to 262 B.C. : Plates*.
Verlag der Österreichischen Akademie der Wissenschaften, 1988.
