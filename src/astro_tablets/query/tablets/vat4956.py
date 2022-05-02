from enum import Enum, unique
from typing import List, Optional

from astro_tablets.constants import (
    ALCYONE,
    ANTARES,
    ARIES,
    AURIGA,
    BETA_CAPRICORNI,
    BETA_GEMINORUM,
    BETA_LIBRAE,
    BETA_VIRGINIS,
    CANCER,
    CAPRICORNUS,
    CUBIT,
    FINGER,
    FORTY_TWO_CANCRI,
    GEMINI,
    JUPITER,
    LEO,
    MARS,
    MERCURY,
    MOON,
    PISCES,
    REGULUS,
    SAGITTARIUS,
    SATURN,
    TAURUS,
    THETA_LEONIS,
    VENUS,
    TimePrecision,
)
from astro_tablets.data import AstroData
from astro_tablets.generate.angular_separation import EclipticPosition
from astro_tablets.generate.planet_events import (
    InnerPlanetPhenomena,
    OuterPlanetPhenomena,
)
from astro_tablets.query.abstract_query import AbstractQuery, SearchRange
from astro_tablets.query.abstract_tablet import (
    AbstractTablet,
    Intercalary,
    MonthLength,
    MonthResult,
    YearToTest,
)
from astro_tablets.query.angular_separation_query import AngularSeparationQuery
from astro_tablets.query.database import BabylonianDay, Database
from astro_tablets.query.halo_query import HaloQuery
from astro_tablets.query.lunar_eclipse_query import (
    ExpectedEclipseType,
    LunarEclipseQuery,
)
from astro_tablets.query.lunar_six_query import LunarSix, LunarSixQuery
from astro_tablets.query.planetary_event_query import PlanetaryEventQuery


@unique
class VAT4956Mode(Enum):
    ALL = "All"
    LUNAR_ONLY = "Lunar Only"
    LUNAR_SIX_ONLY = "Lunar Six Only"
    PLANET_ONLY = "Planetary Only"


class VAT4956(AbstractTablet):
    def year_37_month_1(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[AbstractQuery] = []

        # Sîn (Moon) appeared behind the Bull of Heaven (Taurus)
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.LUNAR_ONLY:
            res.append(
                AngularSeparationQuery(
                    self.db,
                    MOON,
                    TAURUS.central_star,
                    0,
                    TAURUS.radius,
                    EclipticPosition.BEHIND,
                    SearchRange.for_night(month, 1),
                )
            )

        # Kajjamānu (Saturn) was in front of the Swallow (Pisces).
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.PLANET_ONLY:
            res.append(
                AngularSeparationQuery(
                    self.db,
                    SATURN,
                    PISCES.central_star,
                    0,
                    PISCES.radius,
                    EclipticPosition.AHEAD,
                    SearchRange.for_night(month, 1),
                )
            )

        # the 9th, beginning of the night, Sîn (Moon) stood 1 cubit in front of the Rear Foot of the Lion (β Virginis).
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.LUNAR_ONLY:
            res.append(
                AngularSeparationQuery(
                    self.db,
                    MOON,
                    BETA_VIRGINIS,
                    1 * CUBIT,
                    6 * FINGER,
                    EclipticPosition.AHEAD,
                    SearchRange.for_night(month, 9),
                )
            )

        #  The 11th] or the 12th Sagmegar (Jupiter) ‘rose to daylight’ (AR).
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.PLANET_ONLY:
            res.append(
                PlanetaryEventQuery(
                    self.db,
                    JUPITER,
                    OuterPlanetPhenomena.AR,
                    SearchRange.range_of_nights(month, 11, 12),
                )
            )

        #  NA (sunrise to moonset) was 4.
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.LUNAR_SIX_ONLY:
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.NA, 4.0))

        return res

    def year_37_month_2(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[AbstractQuery] = []

        # Sîn (Moon) appeared below the Rear Bright Star of the Large Twins (β Geminorum)
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.LUNAR_ONLY:
            res.append(
                AngularSeparationQuery(
                    self.db,
                    MOON,
                    BETA_GEMINORUM,
                    0,
                    15,
                    EclipticPosition.BELOW,
                    SearchRange.for_night(month, 1),
                )
            )

        # Kajjamānu (Saturn) was in front of the Swallow (Pisces).
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.PLANET_ONLY:
            res.append(
                AngularSeparationQuery(
                    self.db,
                    SATURN,
                    PISCES.central_star,
                    0,
                    PISCES.radius,
                    EclipticPosition.AHEAD,
                    SearchRange.for_night(month, 1),
                )
            )

        # The 3rd, Ṣalbaṭānu (Mars) entered the Crab (Praesepe), the 5th it emerged.
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.PLANET_ONLY:
            res.append(
                AngularSeparationQuery(
                    self.db,
                    MARS,
                    FORTY_TWO_CANCRI,
                    0,
                    5,
                    None,
                    SearchRange.range_of_nights(month, 3, 5),
                )
            )

        # The 10th, Šiḫṭu (Mercury) [rose] in the west behind the [Little] Twins [...] (Gemini)
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.PLANET_ONLY:
            res.append(
                PlanetaryEventQuery(
                    self.db,
                    MERCURY,
                    InnerPlanetPhenomena.EF,
                    SearchRange.for_night_and_day(month, 10),
                )
            )
            res.append(
                AngularSeparationQuery(
                    self.db,
                    MERCURY,
                    GEMINI.central_star,
                    0,
                    GEMINI.radius,
                    None,
                    SearchRange.for_night_and_day(month, 10),
                )
            )

        # The 18th, Dilbat (Venus) was ‘balanced’ 1 cubit 4 fingers above the King (Regulus).
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.PLANET_ONLY:
            res.append(
                AngularSeparationQuery(
                    self.db,
                    VENUS,
                    REGULUS,
                    (1 * CUBIT) + (4 * FINGER),
                    8 * CUBIT,
                    EclipticPosition.ABOVE,
                    SearchRange.for_night(month, 18),
                )
            )

        #  The 26th (KUR) (moonrise to sunrise) was 23, I did not observe Sîn.
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.LUNAR_SIX_ONLY:
            res.append(
                LunarSixQuery(self.db, month, 26, LunarSix.KUR, 23, TimePrecision.LOW)
            )

        return res

    def year_37_month_3(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[AbstractQuery] = []
        # Sîn (Moon) appeared behind the Crab (Cancer);
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.LUNAR_ONLY:
            res.append(
                AngularSeparationQuery(
                    self.db,
                    MOON,
                    CANCER.central_star,
                    0,
                    CANCER.radius,
                    EclipticPosition.BEHIND,
                    SearchRange.for_night(month, 1),
                )
            )

        # NA (sunset to moonset) was 20
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.LUNAR_SIX_ONLY:
            res.append(LunarSixQuery(self.db, month, 1, LunarSix.NA1, 20))

        # At that time, Ṣalba-ṭānu (Mars) and Šiḫṭu (Mercury) were 4 cubits in front of the K[ing ...] (Regulus)
        # In the evening, Šiḫṭu (Mercury) passed below Ṣalbaṭānu (Mars)
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.PLANET_ONLY:
            res.append(
                AngularSeparationQuery(
                    self.db,
                    MARS,
                    REGULUS,
                    4 * CUBIT,
                    1 * CUBIT,
                    EclipticPosition.AHEAD,
                    SearchRange.for_night(month, 1),
                )
            )
            res.append(
                AngularSeparationQuery(
                    self.db,
                    MERCURY,
                    REGULUS,
                    4 * CUBIT,
                    1 * CUBIT,
                    EclipticPosition.AHEAD,
                    SearchRange.for_night(month, 1),
                )
            )
            res.append(
                AngularSeparationQuery(
                    self.db,
                    MARS,
                    MERCURY,
                    0,
                    10,
                    EclipticPosition.ABOVE,
                    SearchRange.for_night(month, 1),
                )
            )

        # Sagmegar (Jupiter) was above Lisi (Antares)
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.PLANET_ONLY:
            res.append(
                (
                    AngularSeparationQuery(
                        self.db,
                        JUPITER,
                        ANTARES,
                        0,
                        15,
                        EclipticPosition.ABOVE,
                        SearchRange.for_night(month, 1),
                    )
                )
            )

        #  Dilbat (Venus) was in the west, opposite the Tail of the Li[on ...] (θ Leonis)
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.PLANET_ONLY:
            res.append(
                AngularSeparationQuery(
                    self.db,
                    VENUS,
                    THETA_LEONIS,
                    0,
                    15,
                    None,
                    SearchRange.for_night(month, 1),
                )
            )

        # Night of the 5th, beginning of the night, Sîn (Moon) passed towards the east 1 cubit ‹above/below›
        # the Bright Star at the Tip of the Lion’s Foot. (Leo)
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.LUNAR_ONLY:
            res.append(
                AngularSeparationQuery(
                    self.db,
                    MOON,
                    LEO.central_star,
                    0,
                    LEO.radius,
                    None,
                    SearchRange.for_night(month, 5),
                )
            )

        # the 8th, evening watch, Sîn (Moon) stood 2 1/2 cubits below the Northern Part of the Scales (β Librae).
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.LUNAR_ONLY:
            res.append(
                AngularSeparationQuery(
                    self.db,
                    MOON,
                    BETA_LIBRAE,
                    2.5 * CUBIT,
                    1 * CUBIT,
                    EclipticPosition.BELOW,
                    SearchRange.for_night(month, 8),
                )
            )

        # Night of the 10th, evening watch, Sîn (Moon) was ‘balanced’ 3 1/2 cubits above Lisi (Antares).
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.LUNAR_ONLY:
            res.append(
                AngularSeparationQuery(
                    self.db,
                    MOON,
                    ANTARES,
                    3.5 * CUBIT,
                    1 * CUBIT,
                    EclipticPosition.ABOVE,
                    SearchRange.for_night(month, 10),
                )
            )

        # The 12th, Ṣalbaṭānu (Mars) was 2/3 of a cubit ˹above˺ [the King ...] (Regulus)
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.PLANET_ONLY:
            res.append(
                AngularSeparationQuery(
                    self.db,
                    MARS,
                    REGULUS,
                    2 / 3 * CUBIT,
                    6 * FINGER,
                    EclipticPosition.ABOVE,
                    SearchRange.for_night(month, 12),
                )
            )

        # The 15th, (one) god was seen with the (other) god, NA (sunrise to moonset) was 7;30
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.LUNAR_SIX_ONLY:
            res.append(LunarSixQuery(self.db, month, 15, LunarSix.NA, 7.5))

        # An eclipse of Sîn (Moon) which passed by
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.LUNAR_ONLY:
            res.append(
                LunarEclipseQuery(
                    self.db,
                    None,
                    ExpectedEclipseType.UNKNOWN,
                    None,
                    None,
                    SearchRange.for_night_and_day(month, 15),
                )
            )
        return res

    def year_37_month_10(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[AbstractQuery] = []
        # The 19th, Dilbat (Venus) was below the Middle Star of the Horn of the Goat [...] (β Capricorni)
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.PLANET_ONLY:
            res.append(
                AngularSeparationQuery(
                    self.db,
                    VENUS,
                    BETA_CAPRICORNI,
                    0,
                    15,
                    EclipticPosition.BELOW,
                    SearchRange.for_night(month, 19),
                )
            )
        return res

    def year_37_month_11(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[AbstractQuery] = []
        # Sîn (Moon) appeared in the Swallow (Pisces)
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.LUNAR_ONLY:
            res.append(
                AngularSeparationQuery(
                    self.db,
                    MOON,
                    PISCES.central_star,
                    0,
                    PISCES.radius,
                    None,
                    SearchRange.for_night(month, 1),
                )
            )

        #  NA (sunset to moonset) was 14;30
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.LUNAR_SIX_ONLY:
            res.append(LunarSixQuery(self.db, month, 1, LunarSix.NA1, 14.5))

        # At that time, Sagmegar (Jupiter) was behind the Elbow of Pabi[lsag by ... cubits ...] (Sagittarius)
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.PLANET_ONLY:
            res.append(
                AngularSeparationQuery(
                    self.db,
                    JUPITER,
                    SAGITTARIUS.central_star,
                    0,
                    SAGITTARIUS.radius,
                    EclipticPosition.BEHIND,
                    SearchRange.for_night(month, 1),
                )
            )

        # The 4th, Dilbat (Venus) was ‘balanced’ 1/2 cubit below the Goat-Fish. (Capricorn)
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.PLANET_ONLY:
            res.append(
                AngularSeparationQuery(
                    self.db,
                    VENUS,
                    CAPRICORNUS.central_star,
                    0,
                    CAPRICORNUS.radius,
                    EclipticPosition.BELOW,
                    SearchRange.for_night(month, 4),
                )
            )

        #  Night of the 6th, evening watch, Sîn (Moon) was surrounded by a ‘fold’ (Halo), the Bristle (Pleiades),
        #  the Bull of Heaven (Taurus), the Chariot (Auriga) [stood within the ‘fold’ ...]
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.LUNAR_ONLY:
            res.append(
                HaloQuery(self.db, MOON, ALCYONE, SearchRange.for_night(month, 6))
            )
            res.append(
                AngularSeparationQuery(
                    self.db,
                    MOON,
                    TAURUS.central_star,
                    0,
                    TAURUS.radius,
                    None,
                    SearchRange.for_night(month, 6),
                )
            )
            res.append(
                AngularSeparationQuery(
                    self.db,
                    MOON,
                    AURIGA.central_star,
                    0,
                    AURIGA.radius,
                    None,
                    SearchRange.for_night(month, 6),
                )
            )

        # Sîn (Moon) was surrounded by a ‘fold’ (Halo); the Lion (Leo) and the Crab (Cancer) were inside the ‘fold’.
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.LUNAR_ONLY:
            res.append(
                AngularSeparationQuery(
                    self.db,
                    MOON,
                    LEO.central_star,
                    0,
                    LEO.radius,
                    None,
                    SearchRange.range_of_nights(month, 7, 15),
                )
            )
            res.append(
                AngularSeparationQuery(
                    self.db,
                    MOON,
                    CANCER.central_star,
                    0,
                    CANCER.radius,
                    None,
                    SearchRange.range_of_nights(month, 7, 15),
                )
            )

        # The King (Regulus) was ‘balanced’ 1 cubit below Sîn (Moon).
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.LUNAR_ONLY:
            res.append(
                AngularSeparationQuery(
                    self.db,
                    REGULUS,
                    MOON,
                    1 * CUBIT,
                    6 * FINGER,
                    EclipticPosition.BELOW,
                    SearchRange.range_of_nights(month, 7, 15),
                )
            )
        return res

    def year_37_month_12(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[AbstractQuery] = []
        # Addaru, the 1st, Sîn (Moon) appeared behind the Hired Man (Aries) while Šamaš was present
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.LUNAR_ONLY:
            res.append(
                AngularSeparationQuery(
                    self.db,
                    MOON,
                    ARIES.central_star,
                    0,
                    ARIES.radius,
                    EclipticPosition.BEHIND,
                    SearchRange.for_night(month, 1),
                )
            )

        # NA (sunset to moonset) was 25
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.LUNAR_SIX_ONLY:
            res.append(LunarSixQuery(self.db, month, 1, LunarSix.NA1, 25))

        # Night of the 2nd, the evening watch, Sîn (Moon) was ‘balanced’ 4 cubits below the Stars (Pleiades).
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.LUNAR_ONLY:
            res.append(
                AngularSeparationQuery(
                    self.db,
                    MOON,
                    ALCYONE,
                    4 * CUBIT,
                    1 * CUBIT,
                    EclipticPosition.BELOW,
                    SearchRange.for_night(month, 2),
                )
            )

        # Night of the 7th, Sîn (Moon) was surrounded by a ‘fold’ (Halo), the Crab (Cancer) and the
        # King (Regulus) were within [the ‘fold’, ...]
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.LUNAR_ONLY:
            res.append(
                AngularSeparationQuery(
                    self.db,
                    MOON,
                    CANCER.central_star,
                    0,
                    CANCER.radius,
                    None,
                    SearchRange.for_night(month, 7),
                )
            )
            res.append(
                HaloQuery(self.db, REGULUS, MOON, SearchRange.for_night(month, 7))
            )

        # The 12th, one god was seen with the (other) god, NA (sunrise to moonset) was 1;30.
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.LUNAR_SIX_ONLY:
            res.append(LunarSixQuery(self.db, month, 12, LunarSix.NA, 1.5))

        # was in front of the Band of the Swallow (Pisces), 1/2 cubit below Dilbat (Venus), Šiḫṭu (Mercury) passing
        # 8 fingers to the east, when it appeared it was bright and high. 1 U[Š ... Kajjamānu (Saturn)] was ‘balanced’
        # 6 fingers above Šiḫṭu (Mercury) and 3 fingers below Dilbat (Venus)
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.PLANET_ONLY:
            res.append(
                AngularSeparationQuery(
                    self.db,
                    VENUS,
                    MERCURY,
                    1 * CUBIT,
                    6 * FINGER,
                    None,
                    SearchRange.range_of_nights(month, 13, 21),
                )
            )

        # Around the 20th Dilbat (Venus) and Šiḫṭu (Mercury) entered the Band of the Swallow (Pisces).
        if self.mode == VAT4956Mode.ALL or self.mode == VAT4956Mode.PLANET_ONLY:
            res.append(
                AngularSeparationQuery(
                    self.db,
                    VENUS,
                    PISCES.central_star,
                    0,
                    PISCES.radius,
                    None,
                    SearchRange.for_night(month, 20),
                )
            )
            res.append(
                AngularSeparationQuery(
                    self.db,
                    MERCURY,
                    PISCES.central_star,
                    0,
                    PISCES.radius,
                    None,
                    SearchRange.for_night(month, 20),
                )
            )
        return res

    def year_37(self, nisan_1: float) -> List[MonthResult]:
        month_i = self.repeat_month_with_alternate_starts(
            nisan_1, 1, self.year_37_month_1, length=MonthLength.THIRTY
        )
        month_ii = self.repeat_month_with_alternate_starts(
            nisan_1, 2, self.year_37_month_2, length=MonthLength.TWENTY_NINE
        )
        month_iii = self.repeat_month_with_alternate_starts(
            nisan_1, 3, self.year_37_month_3
        )
        month_x = self.repeat_month_with_alternate_starts(
            nisan_1, 10, self.year_37_month_10, length=MonthLength.TWENTY_NINE
        )
        month_xi = self.repeat_month_with_alternate_starts(
            nisan_1, 11, self.year_37_month_11, length=MonthLength.THIRTY
        )
        month_xii = self.repeat_month_with_alternate_starts(
            nisan_1, 12, self.year_37_month_12
        )
        return [month_i, month_ii, month_iii, month_x, month_xi, month_xii]

    def __init__(self, data: AstroData, db: Database, subquery: Optional[str]):
        if subquery is None:
            self.mode = VAT4956Mode.ALL
        elif subquery == "lunar_only":
            self.mode = VAT4956Mode.LUNAR_ONLY
        elif subquery == "lunar_six_only":
            self.mode = VAT4956Mode.LUNAR_SIX_ONLY
        elif subquery == "planet_only":
            self.mode = VAT4956Mode.PLANET_ONLY
        else:
            raise ValueError("Unknown subquery")
        title = "Nebuchadnezzar 37 ({})".format(self.mode.value)
        tests = [YearToTest(0, "Nebuchadnezzar 37", Intercalary.FALSE, self.year_37)]
        super().__init__(data, db, tests, title)
