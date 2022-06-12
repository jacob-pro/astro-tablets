from enum import Enum, unique
from typing import List, Optional

from astro_tablets.constants import (
    AURIGA,
    CANCER,
    CUBIT,
    FINGER,
    GEMINI,
    JUPITER,
    LEO,
    LIBRA,
    MARS,
    MERCURY,
    MOON,
    PISCES,
    REGULUS,
    SATURN,
    VENUS,
    VIRGO,
    Precision,
    Radius,
    Watch,
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
from astro_tablets.query.lunar_eclipse_query import (
    ExpectedEclipseType,
    FirstContactRelative,
    FirstContactTime,
    LunarEclipseQuery,
)
from astro_tablets.query.lunar_six_query import LunarSix, LunarSixQuery
from astro_tablets.query.planetary_event_query import PlanetaryEventQuery
from astro_tablets.query.radius_query import WithinRadiusQuery


@unique
class BM33066Mode(Enum):
    ALL = "All"
    ECLIPSE_ONLY = "Eclipses Only"
    LUNAR_SIX_ONLY = "Lunar Six Only"
    PLANET_ONLY = "Planetary Only"


class BM33066(AbstractTablet):
    def year_7_month_1(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[AbstractQuery] = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.LUNAR_SIX_ONLY:
            res.append(LunarSixQuery(self.db, month, 1, LunarSix.NA1, 30))
            res.append(LunarSixQuery(self.db, month, 13, LunarSix.ME, 9))
            res.append(LunarSixQuery(self.db, month, 13, LunarSix.SU2, 2.5))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.GI6, 8 + 1 / 3))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.NA, 7 + 2 / 3))
            res.append(LunarSixQuery(self.db, month, 27, LunarSix.KUR, 16))

        return res

    def year_7_month_2(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[AbstractQuery] = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.LUNAR_SIX_ONLY:
            res.append(LunarSixQuery(self.db, month, 1, LunarSix.NA1, 23))
            res.append(LunarSixQuery(self.db, month, 13, LunarSix.SU2, 8 + 2 / 3))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.ME, 1))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.NA, 1 + 2 / 3))
            res.append(LunarSixQuery(self.db, month, 15, LunarSix.GI6, 14.5))
            res.append(LunarSixQuery(self.db, month, 27, LunarSix.KUR, 21))

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.PLANET_ONLY:
            res.append(
                PlanetaryEventQuery(
                    self.db,
                    MARS,
                    OuterPlanetPhenomena.LA,
                    SearchRange.for_night(month, 28),
                )
            )
            res.append(
                WithinRadiusQuery(
                    self.db,
                    MARS,
                    GEMINI.central_star,
                    GEMINI.radius,
                    EclipticPosition.AHEAD,
                    SearchRange.for_night(month, 28),
                )
            )

        return res

    def year_7_month_3(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[AbstractQuery] = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.LUNAR_SIX_ONLY:
            res.append(LunarSixQuery(self.db, month, 1, LunarSix.NA1, 18.5))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.ME, 9.5))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.SU2, 4))
            res.append(LunarSixQuery(self.db, month, 15, LunarSix.GI6, 5))
            res.append(LunarSixQuery(self.db, month, 15, LunarSix.NA, 8.5))
            res.append(LunarSixQuery(self.db, month, 27, LunarSix.KUR, 15))

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.PLANET_ONLY:
            res.append(
                PlanetaryEventQuery(
                    self.db,
                    VENUS,
                    InnerPlanetPhenomena.EL,
                    SearchRange.for_night(month, 10),
                )
            )
            res.append(
                WithinRadiusQuery(
                    self.db,
                    VENUS,
                    LEO.central_star,
                    LEO.radius,
                    None,
                    SearchRange.for_night(month, 10),
                )
            )
            res.append(
                PlanetaryEventQuery(
                    self.db,
                    VENUS,
                    InnerPlanetPhenomena.MF,
                    SearchRange.for_night(month, 27),
                )
            )
            res.append(
                WithinRadiusQuery(
                    self.db,
                    VENUS,
                    CANCER.central_star,
                    CANCER.radius,
                    None,
                    SearchRange.for_night(month, 27),
                )
            )

        return res

    def year_7_month_4(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[AbstractQuery] = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.LUNAR_SIX_ONLY:
            res.append(LunarSixQuery(self.db, month, 1, LunarSix.NA1, 27))
            res.append(LunarSixQuery(self.db, month, 13, LunarSix.SU2, 11))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.ME, 4))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.NA, 4))
            res.append(LunarSixQuery(self.db, month, 15, LunarSix.GI6, 8.5))
            res.append(LunarSixQuery(self.db, month, 27, LunarSix.KUR, 15))

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.ECLIPSE_ONLY:
            t = (1 + 2 / 3) * 30
            res.append(
                LunarEclipseQuery(
                    self.db,
                    FirstContactTime(t, FirstContactRelative.AFTER_SUNSET),
                    ExpectedEclipseType.TOTAL,
                    None,
                    None,
                    SearchRange.for_night(month, 14),
                )
            )

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.PLANET_ONLY:
            # Year 7, month IV, the 1st, the moon became visible 3 cubits behind Mercury.
            res.append(
                AngularSeparationQuery(
                    self.db,
                    MOON,
                    MERCURY,
                    3 * CUBIT,
                    EclipticPosition.BEHIND,
                    SearchRange.for_night(month, 1),
                )
            )

        return res

    def year_7_month_5(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[AbstractQuery] = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.LUNAR_SIX_ONLY:
            res.append(
                LunarSixQuery(self.db, month, 1, LunarSix.NA1, 10, Precision.LOW)
            )
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.SU2, 3.5))
            res.append(
                LunarSixQuery(self.db, month, 15, LunarSix.ME, 2.5, Precision.LOW)
            )
            res.append(LunarSixQuery(self.db, month, 15, LunarSix.NA, 11))
            res.append(LunarSixQuery(self.db, month, 16, LunarSix.GI6, 7.5))
            res.append(LunarSixQuery(self.db, month, 27, LunarSix.KUR, 22.5))

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.PLANET_ONLY:
            res.append(
                PlanetaryEventQuery(
                    self.db,
                    JUPITER,
                    OuterPlanetPhenomena.LA,
                    SearchRange.for_night(month, 22),
                )
            )
            res.append(
                WithinRadiusQuery(
                    self.db,
                    JUPITER,
                    VIRGO.central_star,
                    VIRGO.radius,
                    EclipticPosition.AHEAD,
                    SearchRange.for_night(month, 22),
                )
            )

        return res

    def year_7_month_6(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[AbstractQuery] = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.LUNAR_SIX_ONLY:
            res.append(LunarSixQuery(self.db, month, 1, LunarSix.NA1, 15 + 2 / 3))
            res.append(LunarSixQuery(self.db, month, 13, LunarSix.SU2, 11))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.NA, 4))
            res.append(LunarSixQuery(self.db, month, 15, LunarSix.ME, 1 + 1 / 3))
            res.append(LunarSixQuery(self.db, month, 16, LunarSix.GI6, 8 + 2 / 3))
            res.append(LunarSixQuery(self.db, month, 28, LunarSix.KUR, 15))

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.PLANET_ONLY:
            res.append(
                PlanetaryEventQuery(
                    self.db,
                    JUPITER,
                    OuterPlanetPhenomena.FA,
                    SearchRange.for_night(month, 22),
                )
            )
            res.append(
                WithinRadiusQuery(
                    self.db,
                    JUPITER,
                    VIRGO.central_star,
                    VIRGO.radius,
                    EclipticPosition.BEHIND,
                    SearchRange.for_night(month, 22),
                )
            )
            res.append(
                PlanetaryEventQuery(
                    self.db,
                    SATURN,
                    OuterPlanetPhenomena.LA,
                    SearchRange.for_night(month, 3),
                )
            )
            res.append(
                WithinRadiusQuery(
                    self.db,
                    SATURN,
                    VIRGO.central_star,
                    VIRGO.radius,
                    None,
                    SearchRange.for_night(month, 3),
                )
            )
            res.append(
                PlanetaryEventQuery(
                    self.db,
                    MARS,
                    OuterPlanetPhenomena.FA,
                    SearchRange.for_night(month, 13),
                )
            )
            res.append(
                WithinRadiusQuery(
                    self.db,
                    MARS,
                    LEO.central_star,
                    LEO.radius,
                    None,
                    SearchRange.for_night(month, 13),
                )
            )

            #  Month VI, the 24th, Venus was 1 +[x cubits?] above Mars.
            res.append(
                AngularSeparationQuery(
                    self.db,
                    VENUS,
                    MARS,
                    1 * CUBIT,
                    EclipticPosition.ABOVE,
                    SearchRange.for_night(month, 24),
                    Precision.LOW,
                )
            )

        return res

    def year_7_month_7(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[AbstractQuery] = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.LUNAR_SIX_ONLY:
            res.append(LunarSixQuery(self.db, month, 1, LunarSix.NA1, 16 + 2 / 3))
            res.append(LunarSixQuery(self.db, month, 13, LunarSix.SU2, 6.5))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.ME, 7.5))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.NA, 12))
            res.append(LunarSixQuery(self.db, month, 15, LunarSix.GI6, 3))
            res.append(LunarSixQuery(self.db, month, 26, LunarSix.KUR, 22))

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.PLANET_ONLY:
            res.append(
                PlanetaryEventQuery(
                    self.db,
                    SATURN,
                    OuterPlanetPhenomena.FA,
                    SearchRange.for_night(month, 13),
                )
            )
            res.append(
                WithinRadiusQuery(
                    self.db,
                    SATURN,
                    VIRGO.central_star,
                    VIRGO.radius,
                    EclipticPosition.BEHIND,
                    SearchRange.for_night(month, 13),
                )
            )

            # Month VII, the 23rd, last part of the night, Jupiter was 3 cubits above the moon.
            res.append(
                AngularSeparationQuery(
                    self.db,
                    JUPITER,
                    MOON,
                    3 * CUBIT,
                    EclipticPosition.ABOVE,
                    SearchRange.for_night_watch(month, 23, Watch.LAST),
                )
            )

            # Month VII, the 29th, last part of the night, Venus on the north side [came near?] 2 fingers to Ju[piter].
            res.append(
                AngularSeparationQuery(
                    self.db,
                    VENUS,
                    JUPITER,
                    2 * FINGER,
                    None,
                    SearchRange.for_night_watch(month, 29, Watch.LAST),
                )
            )

            # Month VII, the 12th, Saturn was 1 cubit in front of Jupiter.
            res.append(
                AngularSeparationQuery(
                    self.db,
                    SATURN,
                    JUPITER,
                    1 * CUBIT,
                    EclipticPosition.AHEAD,
                    SearchRange.for_night(month, 12),
                )
            )

            # Month VII, the 11th, Mars came near to Jupiter 2 fingers.
            res.append(
                AngularSeparationQuery(
                    self.db,
                    MARS,
                    JUPITER,
                    2 * FINGER,
                    None,
                    SearchRange.for_night(month, 11),
                )
            )

        return res

    def year_7_month_8(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[AbstractQuery] = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.LUNAR_SIX_ONLY:
            res.append(LunarSixQuery(self.db, month, 1, LunarSix.NA1, 12 + 2 / 3))
            res.append(LunarSixQuery(self.db, month, 13, LunarSix.SU2, 15))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.NA, 5))
            res.append(LunarSixQuery(self.db, month, 15, LunarSix.ME, 1))
            res.append(LunarSixQuery(self.db, month, 16, LunarSix.GI6, 14))
            res.append(LunarSixQuery(self.db, month, 28, LunarSix.KUR, 26))

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.PLANET_ONLY:
            # Month VIII, the 2nd, Saturn passed 8 fingers above Venus.
            res.append(
                AngularSeparationQuery(
                    self.db,
                    SATURN,
                    VENUS,
                    8 * FINGER,
                    EclipticPosition.ABOVE,
                    SearchRange.for_night(month, 2),
                )
            )

        return res

    def year_7_month_10(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[AbstractQuery] = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.ECLIPSE_ONLY:
            t = (2 + 1 / 2) * 30
            res.append(
                LunarEclipseQuery(
                    self.db,
                    FirstContactTime(t, FirstContactRelative.BEFORE_SUNRISE),
                    ExpectedEclipseType.TOTAL,
                    None,
                    None,
                    SearchRange.for_night(month, 14),
                )
            )

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.PLANET_ONLY:
            res.append(
                PlanetaryEventQuery(
                    self.db,
                    JUPITER,
                    OuterPlanetPhenomena.ST,
                    SearchRange.for_night(month, 27),
                )
            )
            res.append(
                WithinRadiusQuery(
                    self.db,
                    JUPITER,
                    LIBRA.central_star,
                    LIBRA.radius,
                    EclipticPosition.AHEAD,
                    SearchRange.for_night(month, 27),
                )
            )

            # Month X, the 5th, Mercury was ½ cubit behind Venus.
            res.append(
                AngularSeparationQuery(
                    self.db,
                    MERCURY,
                    VENUS,
                    0.5 * CUBIT,
                    EclipticPosition.BEHIND,
                    SearchRange.for_night(month, 5),
                )
            )

        return res

    def year_7_month_11(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[AbstractQuery] = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.LUNAR_SIX_ONLY:
            res.append(LunarSixQuery(self.db, month, 1, LunarSix.NA1, 22))
            res.append(LunarSixQuery(self.db, month, 13, LunarSix.ME, 17 + 1 / 3))
            res.append(LunarSixQuery(self.db, month, 13, LunarSix.SU2, 4 + 2 / 3))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.GI6, 1 + 2 / 3))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.NA, 7))
            res.append(LunarSixQuery(self.db, month, 27, LunarSix.KUR, 17))

        return res

    def year_7_month_12(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[AbstractQuery] = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.LUNAR_SIX_ONLY:
            res.append(LunarSixQuery(self.db, month, 1, LunarSix.NA1, 15.5))
            res.append(LunarSixQuery(self.db, month, 12, LunarSix.SU2, 10.5))
            res.append(LunarSixQuery(self.db, month, 13, LunarSix.ME, 5 + 1 / 3))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.GI6, 10))
            res.append(LunarSixQuery(self.db, month, 25, LunarSix.KUR, 23))
            res.append(LunarSixQuery(self.db, month, 27, LunarSix.KUR, 12))

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.PLANET_ONLY:
            res.append(
                PlanetaryEventQuery(
                    self.db,
                    VENUS,
                    InnerPlanetPhenomena.ML,
                    SearchRange.for_night(month, 7),
                )
            )
            res.append(
                WithinRadiusQuery(
                    self.db,
                    VENUS,
                    PISCES.central_star,
                    PISCES.radius,
                    None,
                    SearchRange.for_night(month, 7),
                )
            )

        return res

    def year_7_month_13(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[AbstractQuery] = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.LUNAR_SIX_ONLY:
            res.append(LunarSixQuery(self.db, month, 1, LunarSix.NA1, 19))
            res.append(
                LunarSixQuery(self.db, month, 13, LunarSix.ME, 1.5, Precision.LOW)
            )
            res.append(LunarSixQuery(self.db, month, 13, LunarSix.SU2, 5 + 1 / 3))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.GI6, 3))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.NA, 5 + 2 / 3))
            res.append(LunarSixQuery(self.db, month, 27, LunarSix.KUR, 21))

        return res

    def year_7(self, nisan_1: float) -> List[MonthResult]:
        month_i = self.repeat_month_with_alternate_starts(
            nisan_1, 1, self.year_7_month_1, length=MonthLength.TWENTY_NINE
        )
        month_ii = self.repeat_month_with_alternate_starts(
            nisan_1, 2, self.year_7_month_2, length=MonthLength.TWENTY_NINE
        )
        month_iii = self.repeat_month_with_alternate_starts(
            nisan_1, 3, self.year_7_month_3, length=MonthLength.THIRTY
        )
        month_iv = self.repeat_month_with_alternate_starts(
            nisan_1, 4, self.year_7_month_4, length=MonthLength.TWENTY_NINE
        )
        month_v = self.repeat_month_with_alternate_starts(
            nisan_1, 5, self.year_7_month_5, length=MonthLength.THIRTY
        )
        month_vi = self.repeat_month_with_alternate_starts(
            nisan_1, 6, self.year_7_month_6, length=MonthLength.THIRTY
        )
        month_vii = self.repeat_month_with_alternate_starts(
            nisan_1, 7, self.year_7_month_7, length=MonthLength.TWENTY_NINE
        )
        month_viii = self.repeat_month_with_alternate_starts(
            nisan_1, 8, self.year_7_month_8
        )
        month_x = self.repeat_month_with_alternate_starts(
            nisan_1, 10, self.year_7_month_10, length=MonthLength.THIRTY
        )
        month_xi = self.repeat_month_with_alternate_starts(
            nisan_1, 11, self.year_7_month_11, length=MonthLength.TWENTY_NINE
        )
        month_xii = self.repeat_month_with_alternate_starts(
            nisan_1, 12, self.year_7_month_12, length=MonthLength.THIRTY
        )
        month_xii2 = self.repeat_month_with_alternate_starts(
            nisan_1, 13, self.year_7_month_13, name="XII2"
        )

        return [
            month_i,
            month_ii,
            month_iii,
            month_iv,
            month_v,
            month_vi,
            month_vii,
            month_viii,
            month_x,
            month_xi,
            month_xii,
            month_xii2,
        ]

    def year_8_month_1(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[AbstractQuery] = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.PLANET_ONLY:
            res.append(
                PlanetaryEventQuery(
                    self.db,
                    VENUS,
                    InnerPlanetPhenomena.EF,
                    SearchRange.for_night(month, 13),
                )
            )
            res.append(
                WithinRadiusQuery(
                    self.db,
                    VENUS,
                    AURIGA.central_star,
                    AURIGA.radius,
                    None,
                    SearchRange.for_night(month, 13),
                )
            )

        return res

    def year_8_month_2(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[AbstractQuery] = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.PLANET_ONLY:
            res.append(
                PlanetaryEventQuery(
                    self.db,
                    JUPITER,
                    OuterPlanetPhenomena.ST,
                    SearchRange.for_night(month, 25),
                )
            )
            res.append(
                WithinRadiusQuery(
                    self.db,
                    JUPITER,
                    VIRGO.central_star,
                    VIRGO.radius,
                    None,
                    SearchRange.for_night(month, 25),
                )
            )

        return res

    def year_8_month_5(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[AbstractQuery] = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.PLANET_ONLY:
            res.append(
                PlanetaryEventQuery(
                    self.db,
                    SATURN,
                    OuterPlanetPhenomena.LA,
                    SearchRange.for_night(month, 29),
                )
            )
            res.append(
                PlanetaryEventQuery(
                    self.db,
                    MARS,
                    OuterPlanetPhenomena.ST,
                    SearchRange.for_night(month, 12),
                )
            )

        return res

    def year_8_month_6(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[AbstractQuery] = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.PLANET_ONLY:
            res.append(
                PlanetaryEventQuery(
                    self.db,
                    JUPITER,
                    OuterPlanetPhenomena.LA,
                    SearchRange.for_night(month, 4),
                )
            )
            res.append(
                WithinRadiusQuery(
                    self.db,
                    JUPITER,
                    LIBRA.central_star,
                    LIBRA.radius,
                    EclipticPosition.BEHIND,
                    SearchRange.for_night(month, 4),
                )
            )

        return res

    def year_8(self, nisan_1: float) -> List[MonthResult]:
        month_i = self.repeat_month_with_alternate_starts(
            nisan_1, 1, self.year_8_month_1
        )
        month_ii = self.repeat_month_with_alternate_starts(
            nisan_1, 2, self.year_8_month_2
        )
        month_v = self.repeat_month_with_alternate_starts(
            nisan_1, 5, self.year_8_month_5
        )
        month_vi = self.repeat_month_with_alternate_starts(
            nisan_1, 6, self.year_8_month_6
        )
        return [month_i, month_ii, month_v, month_vi]

    def year_9_month_2(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[AbstractQuery] = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.PLANET_ONLY:
            #  Year 9, month II, the 9th, last appearance behind α Leonis.
            res.append(
                PlanetaryEventQuery(
                    self.db,
                    MARS,
                    OuterPlanetPhenomena.LA,
                    SearchRange.for_night(month, 9),
                )
            )
            res.append(
                WithinRadiusQuery(
                    self.db,
                    MARS,
                    REGULUS,
                    Radius.MEDIUM.value,
                    EclipticPosition.BEHIND,
                    SearchRange.for_night(month, 9),
                    Precision.LOW,
                )
            )

        return res

    def year_9(self, nisan_1: float) -> List[MonthResult]:
        month_ii = self.repeat_month_with_alternate_starts(
            nisan_1, 2, self.year_9_month_2
        )
        return [month_ii]

    def __init__(self, data: AstroData, db: Database, subquery: Optional[str]):
        if subquery is None:
            self.mode = BM33066Mode.ALL
        elif subquery == "eclipse":
            self.mode = BM33066Mode.ECLIPSE_ONLY
        elif subquery == "lunar_six":
            self.mode = BM33066Mode.LUNAR_SIX_ONLY
        elif subquery == "planet":
            self.mode = BM33066Mode.PLANET_ONLY
        else:
            raise ValueError("Unknown subquery")
        tests = [
            YearToTest(0, "Cambyses 7", Intercalary.ADDARU, self.year_7),
            YearToTest(1, "Cambyses 8", Intercalary.FALSE, self.year_8),
            YearToTest(2, "Cambyses 9", Intercalary.FALSE, self.year_9),
        ]
        title = "Cambyses 7 ({})".format(self.mode.value)
        super().__init__(data, db, tests, title)
