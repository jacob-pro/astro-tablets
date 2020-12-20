# Astro Tablets

A tool designed for dating the events in ancient Babylonian Astronomical Texts
independent from any external assumptions about their chronology. 
(See [Methodology](./documents/methodology.md) for more info about how the tablets are interpreted)

Using the [Skyfield](https://rhodesmill.org/skyfield/) library for Python we 
generate tables of data to covering all the events in a specific tablet. 

The data is saved in an SQLite db which can then be queried for the best match.

## Features

Supported tablets:
- [BM 32312](./documents/bm32312.md)
- [VAT 4956](./documents/vat4956.md)
- [Lunar Text No.3](./documents/lunar3.md)
- [Planetary Text No. 52](./documents/planet52.md)
- [Saturn Tablet](./documents/saturn.md)


Supported features
- Compute a lunar calendar (sunrise, sunset, first visibility, spring equinox)
- Compute angular separation of moon, planets, stars
- Position of two bodies relative to the ecliptic plane
- Compute visibility phenomena of the inner and outer planets

## Setup

- Requires Python 3.5 (note: Skyfield doesn't support newer versions yet)
- Install `requirements.txt`
- When using PyCharm define `./src` as a source folder in project structure
- First run will take a while to download the astronomical data
