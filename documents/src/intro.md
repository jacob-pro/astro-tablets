# Introduction to the Babylonian Astronomical Texts

If you are not familiar with ancient Babylonian Astronomy I recommend reading:

- Teije de Jong's 
  [*Babylonian Astronomy*](https://www.astro.ru.nl/~fverbunt/iac2011/BabAstr.pdf) lecture slides
  from IAC2011 *History of Astronomy* (Radboud, Utrecht, and Amsterdam University) [@dejong2011babylonian].
- The Introduction (pages 11-38) of *Astronomical Diaries and Related Texts Vol. 1* [@sachs1988adt].
- Pages 126-139 of *Translating Babylonian Astronomical Diaries and Procedure Texts* [@ossendrijver2016translating].

## Calendar

> The Babylonians used a luni-solar calendar. The day began at sunset, and each
  month began on the night when the lunar cresent was first visible. There were twelve
  months in most years, each month lasting for 29 or 30 days. To regulate the seasons,
  an intercalary month was inserted when necessary. [@steele1997accuracy, 338]

### Lunar Year

> The beginning of the year, day 1 of Nisannu (month I), always fell within about 30 days of the vernal equinox
> [@ossendrijver2016translating, 131]

The year could either have 12 or 13 months depending on if there was an intercalary month. 
The intercalary month could be either a second Ulūlu (VI₂) or a second Addaru (XII₂).

From the reign of Nabopolassar onwards, I am using the intercalary months 
as documented by Parker and Dubberstein [@dubberstein1956babylonian, 4].

However prior to Nabopolassar the arrangement of intercalary months is not fully complete, 
but I am using this list of confirmed intercalary months [@brinkman1983documentary, 67]:

- Shamash-shum-ukin Year 14, Addaru II: BM 29496, YBC 11309
- Kandalanu Year 5, Ululu II: Clay BE 8/1, No.3, [BM76738](./bm76738_76813.md#translation) Obv. 10
- Kandalanu Year 8, Ululu II: [BM76738](./bm76738_76813.md#translation) Obv. 15
- Kandalanu Year 10, Addaru II: BM 54213, [BM76738](./bm76738_76813.md#translation) Rev. 20
- Kandalanu Year 19, Addaru II: YBC 11481, 11300, 11476, NBC 6144

### Lunar Month

> Day 1 of the new month was declared at the first appearance of the lunar crescent after sunset...
> The only attested month lengths are 29 days and 30 days, because day 1 was declared no later than the sunset at the
> end of day 30, irrespective of whether the crescent was then observed or not. 
> [@ossendrijver2016translating, 131]

In order to compute the start of the month I am using the following lunar visibility parameter:

> Our calculation shows that 7.5° (±0.25°) is the lowest naked eye visibility limit.
> [@sultan2007visibility, 58]

## Angular Separations

The diaries describe the angular separations; the angle between two sightlines from the observer on Earth to two
different celestial bodies in the sky. These are measured in terms of "cubits" and "fingers",
where there are 24 fingers in a cubit. In order to convert to degrees:

> Our results for the angular equivalent of the finger and cubit in the Neo-Babylonian period are respectively 0.092 
> and 2.2 deg
> [@fatoohi1997angular, 212]

The diaries sometimes describe bodies as appearing within a "halo", this is a ring around the moon or sun
with a 22° (or 10 cubit) radius. Haloes can also exist as a 46° ring, but they are not found in the diaries:

> The larger type of halo called supūru is not so far attested in diaries.
> [@sachs1988adt, 33]

### Constellations

Where the tablets describe a body as being within a constellation, I will approximate that position
by drawing an appropriate radius around a relatively central star within that constellation. 
It is only possible to take an approximate approach anyway given 
that the boundaries for ancient constellations have not been strictly defined.

## Planetary Visibilty

Inner Planet (Mercury, Venus) synodic phenomena:

| Translation                  | Name            | Acronym |
|------------------------------|-----------------|---------|
| to appear in the west        | evening first   | EF      |
| to be stationary in the west | evening station | ES      |
| to set in the west           | evening last    | EL      |
| to appear in the east        | morning first   | MF      |
| to be stationary in the east | morning station | MS      |
| to set in the east           | morning last    | ML      |

Outer Planet (Mars, Jupiter, Saturn) synodic phenomena:

| Translation                    | Name              | Acronym |
|--------------------------------|-------------------|---------|
| to appear                      | first appearance  | FA      |
| to be stationary at the first  | first station     | S1      |
| to rise to daylight            | acronychal rising | AR      |
| to be stationary at the second | second station    | S2      |
| to set                         | last appearance   | LA      |

Computing the synodic phenomena requires setting Arcus Visionis parameters:

> the minimum angular distance between the star/planet and the Sun measured 
  perpendicular to the horizon for the star/planet to be visible [@dejong2011babylonian, 38]

I am using the default fixed arcus visionis parameters
from Alcyone Planetary, Stellar and Lunar Visibility [@alcyoneplsv] (see `src/constants.py`).

## Lunar Six Intervals

| Lunar Six | From                                     | To                                     | Taken Near |
|-----------|------------------------------------------|----------------------------------------|------------|
| NA₁       | **sunset**                               | first visible **moonset** after sunset | New Moon   |
| ŠU₂       | last **moonset** before sunrise          | **sunrise**                            | Full Moon  |
| NA        | **sunrise**                              | first **moonset** after sunrise        | Full Moon  |
| ME        | last **moonrise** before sunset          | **sunset**                             | Full Moon  |
| GI₆       | **sunset**                               | first **moonrise** after sunset        | Full Moon  |
| KUR       | last visible **moonrise** before sunrise | **sunrise**                            | New Moon   |

Times are measured in UŠ - "time degrees". There are 360 UŠ in a day, so 1 UŠ = 4 minutes, 
1 bēru = 30 UŠ [@stephenson1994babylonian] [@sachs1988adt, 16]

> The two pairs of visibility phenomena around full moon, the first being 
  ME and GE₆ and the other consisting of ŠÚ and NA, are frequently designated as the
  Lunar Four. [@britton2008remarks, 7]

## Eclipses

> Observations of eclipses by the Babylonian astronomers usually contain the time
  of the eclipse measured relative to sunset or sunrise, the approximate entrance angle
  of the shadow, and an estimate of the eclipse magnitude. In many reports the duration
  of the individual phases of the eclipse are also given. [@steele1997lunar, 120]
  
> It is characteristic for the record of the observation to end with a time. 
  This may be understood as referring to the time of first contact. [@steele1997lunar, 120]

> The eclipse records also contain descriptions of lunar eclipses that proved invisible
  at Babylon. These descriptions must then be predictions rather than observations.
  Usually it is possible to distinguish a predicted eclipse from an observation
  by the terminology used.  [@steele1997lunar, 121]

Some reports include measurements of the eclipse phases, including the time to maximal 
phase (onset), duration of maximal phase (totality), and time from the end of maximal phase
to the end of the eclipse (clearing), or the total length the eclipse which is the sum of
all three phases. [@sachs1988adt, 24]

In the case of a total lunar eclipse, the onset is the time from when the moon becomes
partially eclipsed (1:2) to the start of the full eclipse, the maximal
phase is the time in which it is fully eclipsed (2:3), and the clearing is the time until
it is no longer partially eclipsed (3:4) [@steele1997accuracy, 341]:
![](graphics/total_eclipse.png)

In the case of partial eclipses it is less straightforward, I can measure the time from
the start of the partial eclipse until it becomes maximal (i.e. nearest separation of
the moon and the shadow) (1:M), and the time from then to the end of the eclipse (M:4). But because
there is a continuous curve, it is difficult to define a maximal phase "duration":
![](graphics/partial_eclipse.png)

Therefore in the case of partial eclipses I am only considering the total eclipse duration.

## Translations

The general conventions used for most of the translations [@sachs1988adt, 37]:

- Square brackets `[]` denote missing/reconstructed text
- Half brackets `⌜⌝` denote text damaged in some other way
- A question mark indicates doubts about the reading of a sign

As a general rule I will not rely on reconstructed text for use in analysing the observations; I will treat those
sections as if they were missing. There are some exceptions to this, such as where it is possible to deduce information
about the missing text from its surroundings, for example:

- Where a year/month/day number is missing or damaged I will assume that if the text is in order then the missing
  number will fit within the range of adjacent lines
- [BM76738](./bm76738_76813.md) follows a consistent pattern where every other line is the last/first appearance, 
  and every two lines spans a year.
  
## References
