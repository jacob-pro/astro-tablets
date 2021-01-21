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
- [ ] [BM 41222 (ADT V No.52)](documents/bm41222.md)
- [ ] [BM 76738 and BM 76813](./documents/bm76738.md)
- [ ] [BM 35115 (LBAT 1415-7, ADT V No.3)](documents/bm35115.md)
- [ ] [BM 32234 (LBAT 1419, ADT V No.4)](documents/bm32234.md)
- [ ] [BM 38462 (LBAT 1420, ADT V No.6)](documents/bm38462.md)
- [ ] [VAT 4956](./documents/vat4956.md)
- [ ] [BM 33066 (LBAT 1477, Strm. Kambys. 400)](./documents/bm33066.md)

Supported features
- Compute a lunar calendar (sunrise, sunset, first visibility, spring equinox)
- Angular separation of moon, planets, stars
- Position of two bodies with direction relative to the ecliptic plane
- Visibility phenomena and stations of the inner and outer planets

## Setup

- Requires Python 3
- Install `requirements.txt`
- When using PyCharm define `./src` as a source folder in project structure
- First run will take a while to download the astronomical data

`pypy -m ensurepip`
`pypy3 -mpip install -r requirements.txt`

