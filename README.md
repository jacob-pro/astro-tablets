# Astro Tablets

A tool designed for dating the events in ancient Babylonian Astronomical Texts
whilst making as few assumptions as possible about their chronology. 
(See [Methodology](./documents/methodology.md) for more info about how the texts are interpreted)

Using the [Skyfield](https://rhodesmill.org/skyfield/) library for Python we 
generate tables of data to covering all the events in a specific tablet. 

The data tables are saved in a SQLite db which can then be queried for the best match.

## Features

Support for these texts:
- [X] [BM 32312](./documents/bm32312.md)
- [ ] [VAT 4956](./documents/vat4956.md)
- [ ] [Lunar Text No.3](./documents/lunar3.md)
- [ ] [Planetary Text No. 52](./documents/planet52.md)
- [ ] [Saturn Tablet](./documents/saturn.md)
- [ ] [BM 33066](./documents/bm33066.md)

Supported features
- Compute a lunar calendar (sunrise, sunset, first visibility, spring equinox)
- Angular separation of moon, planets, stars
- Position of two bodies with direction relative to the ecliptic plane
- Visibility phenomena and stations of the inner and outer planets

## Setup

- Requires Python == 3.5 (note: Skyfield doesn't support newer versions yet)
- Install `requirements.txt`
- When using PyCharm define `./src` as a source folder in project structure
- First run will take a while to download the astronomical data
