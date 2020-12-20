# Astro Tablets

A tool designed for dating the events in ancient Babylonian Astronomical Texts
independent from any external assumptions about their chronology. 

## Method

Using the [Skyfield](https://rhodesmill.org/skyfield/) library for Python we 
generate ephemeris data to cover all the events in a specific tablet. 

The ephemeris are saved in SQL tables which can then be queried for the best match.

## Features

Supported tablets:
- BM32312

Supported features
- Compute a lunar calendar
- Compute angular separation of moon, planets, stars
- Position of two bodies relative to the ecliptic plane
- Compute visibility phenomena of inner and outer planets

## Setup

- Requires Python 3.5 (note: Skyfield doesn't support newer versions yet)
- Install `requirements.txt`
- When using PyCharm define `./src` as a source folder in project structure
- First run will take a while to download the astronomical data
