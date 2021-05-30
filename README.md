# Astro Tablets

A tool designed for dating the events in ancient Babylonian Astronomical Texts
whilst making as few assumptions as possible about their chronology. 

See [Introduction](./documents/texts.md) for a background on the texts, and explanations for
how I am interpreting them.

See [Methodology](./documents/methodology.md) to see how the queries / rankings of dates
are calculated.

## Features

Support for these texts:
- [X] [BM 32312](./documents/bm32312.md)
- [X] [BM 41222 (ADT V No.52)](documents/bm41222.md)
- [X] [BM 76738 and 76813](./documents/bm76738_76813.md)
- [ ] [BM 35115... (LBAT 1415-7, ADT V No.3)](documents/bm35115_35789_45640.md)
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

- Requires Python 3.7
- Install `requirements.txt`
- When using PyCharm define `./src` as a source folder in project structure
- First run will take a while to download the astronomical data
