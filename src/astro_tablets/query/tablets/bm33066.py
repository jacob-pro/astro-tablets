from enum import Enum, unique
from typing import List, Optional, Tuple

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
class Category(Enum):
    ECLIPSE = "Eclipses"
    LUNAR_SIX = "Lunar Six"
    PLANETARY = "Planetary"


class BM33066(AbstractTablet):
    def category_filter(
        self, queries: List[Tuple[AbstractQuery, Category]]
    ) -> List[AbstractQuery]:
        queries = list(
            filter(lambda x: self.filter is None or x[1] == self.filter, queries)
        )
        return list(map(lambda x: x[0], queries))

    def year_7_month_1(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[Tuple[AbstractQuery, Category]] = [
            (LunarSixQuery(self.db, month, 1, LunarSix.NA1, 30), Category.LUNAR_SIX),
            (LunarSixQuery(self.db, month, 13, LunarSix.ME, 9), Category.LUNAR_SIX),
            (LunarSixQuery(self.db, month, 13, LunarSix.SU2, 2.5), Category.LUNAR_SIX),
            (
                LunarSixQuery(self.db, month, 14, LunarSix.GI6, 8 + 1 / 3),
                Category.LUNAR_SIX,
            ),
            (
                LunarSixQuery(self.db, month, 14, LunarSix.NA, 7 + 2 / 3),
                Category.LUNAR_SIX,
            ),
            (LunarSixQuery(self.db, month, 27, LunarSix.KUR, 16), Category.LUNAR_SIX),
        ]

        return self.category_filter(res)

    def year_7_month_2(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[Tuple[AbstractQuery, Category]] = [
            (LunarSixQuery(self.db, month, 1, LunarSix.NA1, 23), Category.LUNAR_SIX),
            (
                LunarSixQuery(self.db, month, 13, LunarSix.SU2, 8 + 2 / 3),
                Category.LUNAR_SIX,
            ),
            (LunarSixQuery(self.db, month, 14, LunarSix.ME, 1), Category.LUNAR_SIX),
            (
                LunarSixQuery(self.db, month, 14, LunarSix.NA, 1 + 2 / 3),
                Category.LUNAR_SIX,
            ),
            (LunarSixQuery(self.db, month, 15, LunarSix.GI6, 14.5), Category.LUNAR_SIX),
            (LunarSixQuery(self.db, month, 27, LunarSix.KUR, 21), Category.LUNAR_SIX),
            #  Year 7, month II, the 28th, Mars' last appearance in front of Gemini.
            (
                PlanetaryEventQuery(
                    self.db,
                    MARS,
                    OuterPlanetPhenomena.LA,
                    SearchRange.for_night(month, 28),
                ),
                Category.PLANETARY,
            ),
            (
                WithinRadiusQuery(
                    self.db,
                    MARS,
                    GEMINI.central_star,
                    GEMINI.radius,
                    EclipticPosition.AHEAD,
                    SearchRange.for_night(month, 28),
                ),
                Category.PLANETARY,
            ),
        ]
        return self.category_filter(res)

    def year_7_month_3(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[Tuple[AbstractQuery, Category]] = [
            (LunarSixQuery(self.db, month, 1, LunarSix.NA1, 18.5), Category.LUNAR_SIX),
            (LunarSixQuery(self.db, month, 14, LunarSix.ME, 9.5), Category.LUNAR_SIX),
            (LunarSixQuery(self.db, month, 14, LunarSix.SU2, 4), Category.LUNAR_SIX),
            (LunarSixQuery(self.db, month, 15, LunarSix.GI6, 5), Category.LUNAR_SIX),
            (LunarSixQuery(self.db, month, 15, LunarSix.NA, 8.5), Category.LUNAR_SIX),
            (LunarSixQuery(self.db, month, 27, LunarSix.KUR, 15), Category.LUNAR_SIX),
            #  Year 7, month III, the 10th. Venus' last appearance in the west in the beginning of Leo.
            (
                PlanetaryEventQuery(
                    self.db,
                    VENUS,
                    InnerPlanetPhenomena.EL,
                    SearchRange.for_night(month, 10),
                ),
                Category.PLANETARY,
            ),
            (
                WithinRadiusQuery(
                    self.db,
                    VENUS,
                    LEO.central_star,
                    LEO.radius,
                    None,
                    SearchRange.for_night(month, 10),
                ),
                Category.PLANETARY,
            ),
            #  Month III. the 27th. first appearance in the east in the area of Cancer.
            (
                PlanetaryEventQuery(
                    self.db,
                    VENUS,
                    InnerPlanetPhenomena.MF,
                    SearchRange.for_night(month, 27),
                ),
                Category.PLANETARY,
            ),
            (
                WithinRadiusQuery(
                    self.db,
                    VENUS,
                    CANCER.central_star,
                    CANCER.radius,
                    None,
                    SearchRange.for_night(month, 27),
                ),
                Category.PLANETARY,
            ),
        ]
        return self.category_filter(res)

    def year_7_month_4(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[Tuple[AbstractQuery, Category]] = [
            (LunarSixQuery(self.db, month, 1, LunarSix.NA1, 27), Category.LUNAR_SIX),
            (LunarSixQuery(self.db, month, 13, LunarSix.SU2, 11), Category.LUNAR_SIX),
            (LunarSixQuery(self.db, month, 14, LunarSix.ME, 4), Category.LUNAR_SIX),
            (LunarSixQuery(self.db, month, 14, LunarSix.NA, 4), Category.LUNAR_SIX),
            (LunarSixQuery(self.db, month, 15, LunarSix.GI6, 8.5), Category.LUNAR_SIX),
            (LunarSixQuery(self.db, month, 27, LunarSix.KUR, 15), Category.LUNAR_SIX),
            # Year 7, month IV, night of the 14th, 1 ⅔ bēru after sunset,
            # the moon made a total eclipse, a little remained; the north wind blew.
            (
                LunarEclipseQuery(
                    self.db,
                    FirstContactTime(
                        (1 + 2 / 3) * 30, FirstContactRelative.AFTER_SUNSET
                    ),
                    ExpectedEclipseType.TOTAL,
                    None,
                    None,
                    SearchRange.for_night(month, 14),
                ),
                Category.ECLIPSE,
            ),
            # Year 7, month IV, the 1st, the moon became visible 3 cubits behind Mercury.
            (
                AngularSeparationQuery(
                    self.db,
                    MOON,
                    MERCURY,
                    3 * CUBIT,
                    EclipticPosition.BEHIND,
                    SearchRange.for_night(month, 1),
                ),
                Category.PLANETARY,
            ),
        ]
        return self.category_filter(res)

    def year_7_month_5(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[Tuple[AbstractQuery, Category]] = [
            (
                LunarSixQuery(self.db, month, 1, LunarSix.NA1, 10, Precision.LOW),
                Category.LUNAR_SIX,
            ),
            (LunarSixQuery(self.db, month, 14, LunarSix.SU2, 3.5), Category.LUNAR_SIX),
            (
                LunarSixQuery(self.db, month, 15, LunarSix.ME, 2.5, Precision.LOW),
                Category.LUNAR_SIX,
            ),
            (LunarSixQuery(self.db, month, 15, LunarSix.NA, 11), Category.LUNAR_SIX),
            (LunarSixQuery(self.db, month, 16, LunarSix.GI6, 7.5), Category.LUNAR_SIX),
            (LunarSixQuery(self.db, month, 27, LunarSix.KUR, 22.5), Category.LUNAR_SIX),
            #  Year 7, month V, the 22nd. Jupiter's last appearance in front of Virgo.
            (
                PlanetaryEventQuery(
                    self.db,
                    JUPITER,
                    OuterPlanetPhenomena.LA,
                    SearchRange.for_night(month, 22),
                ),
                Category.PLANETARY,
            ),
            (
                WithinRadiusQuery(
                    self.db,
                    JUPITER,
                    VIRGO.central_star,
                    VIRGO.radius,
                    EclipticPosition.AHEAD,
                    SearchRange.for_night(month, 22),
                ),
                Category.PLANETARY,
            ),
        ]
        return self.category_filter(res)

    def year_7_month_6(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[Tuple[AbstractQuery, Category]] = [
            (
                LunarSixQuery(self.db, month, 1, LunarSix.NA1, 15 + 2 / 3),
                Category.LUNAR_SIX,
            ),
            (LunarSixQuery(self.db, month, 13, LunarSix.SU2, 11), Category.LUNAR_SIX),
            (LunarSixQuery(self.db, month, 14, LunarSix.NA, 4), Category.LUNAR_SIX),
            (
                LunarSixQuery(self.db, month, 15, LunarSix.ME, 1 + 1 / 3),
                Category.LUNAR_SIX,
            ),
            (
                LunarSixQuery(self.db, month, 16, LunarSix.GI6, 8 + 2 / 3),
                Category.LUNAR_SIX,
            ),
            (LunarSixQuery(self.db, month, 28, LunarSix.KUR, 15), Category.LUNAR_SIX),
            #  Month VI, the 22nd, first appearance behind Virgo.
            (
                PlanetaryEventQuery(
                    self.db,
                    JUPITER,
                    OuterPlanetPhenomena.FA,
                    SearchRange.for_night(month, 22),
                ),
                Category.PLANETARY,
            ),
            (
                WithinRadiusQuery(
                    self.db,
                    JUPITER,
                    VIRGO.central_star,
                    VIRGO.radius,
                    EclipticPosition.BEHIND,
                    SearchRange.for_night(month, 22),
                ),
                Category.PLANETARY,
            ),
            #  Year 7, month VI, the 3rd, Saturn's last appearance in the area of Virgo.
            (
                PlanetaryEventQuery(
                    self.db,
                    SATURN,
                    OuterPlanetPhenomena.LA,
                    SearchRange.for_night(month, 3),
                ),
                Category.PLANETARY,
            ),
            (
                WithinRadiusQuery(
                    self.db,
                    SATURN,
                    VIRGO.central_star,
                    VIRGO.radius,
                    None,
                    SearchRange.for_night(month, 3),
                ),
                Category.PLANETARY,
            ),
            # Month VI, the 13th, first appearance in the foot of Leo.
            (
                PlanetaryEventQuery(
                    self.db,
                    MARS,
                    OuterPlanetPhenomena.FA,
                    SearchRange.for_night(month, 13),
                ),
                Category.PLANETARY,
            ),
            (
                WithinRadiusQuery(
                    self.db,
                    MARS,
                    LEO.central_star,
                    LEO.radius,
                    None,
                    SearchRange.for_night(month, 13),
                ),
                Category.PLANETARY,
            ),
            #  Month VI, the 24th, Venus was 1 +[x cubits?] above Mars.
            (
                AngularSeparationQuery(
                    self.db,
                    VENUS,
                    MARS,
                    1 * CUBIT,
                    EclipticPosition.ABOVE,
                    SearchRange.for_night(month, 24),
                    Precision.LOW,
                ),
                Category.PLANETARY,
            ),
        ]
        return self.category_filter(res)

    def year_7_month_7(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[Tuple[AbstractQuery, Category]] = [
            (
                LunarSixQuery(self.db, month, 1, LunarSix.NA1, 16 + 2 / 3),
                Category.LUNAR_SIX,
            ),
            (LunarSixQuery(self.db, month, 13, LunarSix.SU2, 6.5), Category.LUNAR_SIX),
            (LunarSixQuery(self.db, month, 14, LunarSix.ME, 7.5), Category.LUNAR_SIX),
            (LunarSixQuery(self.db, month, 14, LunarSix.NA, 12), Category.LUNAR_SIX),
            (LunarSixQuery(self.db, month, 15, LunarSix.GI6, 3), Category.LUNAR_SIX),
            (LunarSixQuery(self.db, month, 26, LunarSix.KUR, 22), Category.LUNAR_SIX),
            #  Month VII, the 13th, first appearance behind Virgo.
            (
                PlanetaryEventQuery(
                    self.db,
                    SATURN,
                    OuterPlanetPhenomena.FA,
                    SearchRange.for_night(month, 13),
                ),
                Category.PLANETARY,
            ),
            (
                WithinRadiusQuery(
                    self.db,
                    SATURN,
                    VIRGO.central_star,
                    VIRGO.radius,
                    EclipticPosition.BEHIND,
                    SearchRange.for_night(month, 13),
                ),
                Category.PLANETARY,
            ),
            # Month VII, the 23rd, last part of the night, Jupiter was 3 cubits above the moon.
            (
                AngularSeparationQuery(
                    self.db,
                    JUPITER,
                    MOON,
                    3 * CUBIT,
                    EclipticPosition.ABOVE,
                    SearchRange.for_night(month, 23),
                ),
                Category.PLANETARY,
            ),
            # Month VII, the 29th, last part of the night, Venus on the north side [came near?] 2 fingers to Ju[piter].
            (
                AngularSeparationQuery(
                    self.db,
                    VENUS,
                    JUPITER,
                    2 * FINGER,
                    None,
                    SearchRange.for_night(month, 29),
                ),
                Category.PLANETARY,
            ),
            # Month VII, the 12th, Saturn was 1 cubit in front of Jupiter.
            (
                AngularSeparationQuery(
                    self.db,
                    SATURN,
                    JUPITER,
                    1 * CUBIT,
                    EclipticPosition.AHEAD,
                    SearchRange.for_night(month, 12),
                ),
                Category.PLANETARY,
            ),
            # Month VII, the 11th, Mars came near to Jupiter 2 fingers.
            (
                AngularSeparationQuery(
                    self.db,
                    MARS,
                    JUPITER,
                    2 * FINGER,
                    None,
                    SearchRange.for_night(month, 11),
                ),
                Category.PLANETARY,
            ),
        ]
        return self.category_filter(res)

    def year_7_month_8(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[Tuple[AbstractQuery, Category]] = [
            (
                LunarSixQuery(self.db, month, 1, LunarSix.NA1, 12 + 2 / 3),
                Category.LUNAR_SIX,
            ),
            (LunarSixQuery(self.db, month, 13, LunarSix.SU2, 15), Category.LUNAR_SIX),
            (LunarSixQuery(self.db, month, 14, LunarSix.NA, 5), Category.LUNAR_SIX),
            (LunarSixQuery(self.db, month, 15, LunarSix.ME, 1), Category.LUNAR_SIX),
            (LunarSixQuery(self.db, month, 16, LunarSix.GI6, 14), Category.LUNAR_SIX),
            (LunarSixQuery(self.db, month, 28, LunarSix.KUR, 26), Category.LUNAR_SIX),
            # Month VIII, the 2nd, Saturn passed 8 fingers above Venus.
            (
                AngularSeparationQuery(
                    self.db,
                    SATURN,
                    VENUS,
                    8 * FINGER,
                    EclipticPosition.ABOVE,
                    SearchRange.for_night(month, 2),
                ),
                Category.PLANETARY,
            ),
        ]

        return self.category_filter(res)

    def year_7_month_10(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[Tuple[AbstractQuery, Category]] = [
            # Month X, night of the 14th, when 2 ½ bēru remained to sunrise,
            # the moon made a total eclipse; the south and north winds blew in it.
            (
                LunarEclipseQuery(
                    self.db,
                    FirstContactTime(
                        (2 + 1 / 2) * 30, FirstContactRelative.BEFORE_SUNRISE
                    ),
                    ExpectedEclipseType.TOTAL,
                    None,
                    None,
                    SearchRange.for_night(month, 14),
                ),
                Category.ECLIPSE,
            ),
            #  Month X, the 27th, it became stationary in front of Libra.
            (
                PlanetaryEventQuery(
                    self.db,
                    JUPITER,
                    OuterPlanetPhenomena.ST,
                    SearchRange.for_night(month, 27),
                ),
                Category.PLANETARY,
            ),
            (
                WithinRadiusQuery(
                    self.db,
                    JUPITER,
                    LIBRA.central_star,
                    LIBRA.radius,
                    EclipticPosition.AHEAD,
                    SearchRange.for_night(month, 27),
                ),
                Category.PLANETARY,
            ),
            # Month X, the 5th, Mercury was ½ cubit behind Venus.
            (
                AngularSeparationQuery(
                    self.db,
                    MERCURY,
                    VENUS,
                    0.5 * CUBIT,
                    EclipticPosition.BEHIND,
                    SearchRange.for_night(month, 5),
                ),
                Category.PLANETARY,
            ),
        ]
        return self.category_filter(res)

    def year_7_month_11(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[Tuple[AbstractQuery, Category]] = [
            (LunarSixQuery(self.db, month, 1, LunarSix.NA1, 22), Category.LUNAR_SIX),
            (
                LunarSixQuery(self.db, month, 13, LunarSix.ME, 17 + 1 / 3),
                Category.LUNAR_SIX,
            ),
            (
                LunarSixQuery(self.db, month, 13, LunarSix.SU2, 4 + 2 / 3),
                Category.LUNAR_SIX,
            ),
            (
                LunarSixQuery(self.db, month, 14, LunarSix.GI6, 1 + 2 / 3),
                Category.LUNAR_SIX,
            ),
            (LunarSixQuery(self.db, month, 14, LunarSix.NA, 7), Category.LUNAR_SIX),
            (LunarSixQuery(self.db, month, 27, LunarSix.KUR, 17), Category.LUNAR_SIX),
        ]
        return self.category_filter(res)

    def year_7_month_12(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[Tuple[AbstractQuery, Category]] = [
            (LunarSixQuery(self.db, month, 1, LunarSix.NA1, 15.5), Category.LUNAR_SIX),
            (LunarSixQuery(self.db, month, 12, LunarSix.SU2, 10.5), Category.LUNAR_SIX),
            (
                LunarSixQuery(self.db, month, 13, LunarSix.ME, 5 + 1 / 3),
                Category.LUNAR_SIX,
            ),
            (LunarSixQuery(self.db, month, 14, LunarSix.GI6, 10), Category.LUNAR_SIX),
            (LunarSixQuery(self.db, month, 25, LunarSix.KUR, 23), Category.LUNAR_SIX),
            (LunarSixQuery(self.db, month, 27, LunarSix.KUR, 12), Category.LUNAR_SIX),
            #  Month XII, the 7th, last appearance in the east in the area of Pisces.
            (
                PlanetaryEventQuery(
                    self.db,
                    VENUS,
                    InnerPlanetPhenomena.ML,
                    SearchRange.for_night(month, 7),
                ),
                Category.PLANETARY,
            ),
            (
                WithinRadiusQuery(
                    self.db,
                    VENUS,
                    PISCES.central_star,
                    PISCES.radius,
                    None,
                    SearchRange.for_night(month, 7),
                ),
                Category.PLANETARY,
            ),
        ]
        return self.category_filter(res)

    def year_7_month_13(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[Tuple[AbstractQuery, Category]] = [
            (LunarSixQuery(self.db, month, 1, LunarSix.NA1, 19), Category.LUNAR_SIX),
            (
                LunarSixQuery(self.db, month, 13, LunarSix.ME, 1.5, Precision.LOW),
                Category.LUNAR_SIX,
            ),
            (
                LunarSixQuery(self.db, month, 13, LunarSix.SU2, 5 + 1 / 3),
                Category.LUNAR_SIX,
            ),
            (LunarSixQuery(self.db, month, 14, LunarSix.GI6, 3), Category.LUNAR_SIX),
            (
                LunarSixQuery(self.db, month, 14, LunarSix.NA, 5 + 2 / 3),
                Category.LUNAR_SIX,
            ),
            (LunarSixQuery(self.db, month, 27, LunarSix.KUR, 21), Category.LUNAR_SIX),
        ]
        return self.category_filter(res)

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
        res: List[Tuple[AbstractQuery, Category]] = [
            #  Year 8, month I. the 13th. first appearance in the west in the area of the Chariot.
            (
                PlanetaryEventQuery(
                    self.db,
                    VENUS,
                    InnerPlanetPhenomena.EF,
                    SearchRange.for_night(month, 13),
                ),
                Category.PLANETARY,
            ),
            (
                WithinRadiusQuery(
                    self.db,
                    VENUS,
                    AURIGA.central_star,
                    AURIGA.radius,
                    None,
                    SearchRange.for_night(month, 13),
                ),
                Category.PLANETARY,
            ),
        ]

        return self.category_filter(res)

    def year_8_month_2(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[Tuple[AbstractQuery, Category]] = [
            #  Year 8, month II. the 25th, it became stationary in the area of Virgo.
            (
                PlanetaryEventQuery(
                    self.db,
                    JUPITER,
                    OuterPlanetPhenomena.ST,
                    SearchRange.for_night(month, 25),
                ),
                Category.PLANETARY,
            ),
            (
                WithinRadiusQuery(
                    self.db,
                    JUPITER,
                    VIRGO.central_star,
                    VIRGO.radius,
                    None,
                    SearchRange.for_night(month, 25),
                ),
                Category.PLANETARY,
            ),
        ]

        return self.category_filter(res)

    def year_8_month_5(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[Tuple[AbstractQuery, Category]] = [
            #  Year 8, month V, the 29th, last appearance.
            (
                PlanetaryEventQuery(
                    self.db,
                    SATURN,
                    OuterPlanetPhenomena.LA,
                    SearchRange.for_night(month, 29),
                ),
                Category.PLANETARY,
            ),
            (
                PlanetaryEventQuery(
                    self.db,
                    MARS,
                    OuterPlanetPhenomena.ST,
                    SearchRange.for_night(month, 12),
                ),
                Category.PLANETARY,
            ),
        ]

        return self.category_filter(res)

    def year_8_month_6(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res: List[Tuple[AbstractQuery, Category]] = [
            #  Month VI, the 4th, last appearance behind Libra.
            (
                PlanetaryEventQuery(
                    self.db,
                    JUPITER,
                    OuterPlanetPhenomena.LA,
                    SearchRange.for_night(month, 4),
                ),
                Category.PLANETARY,
            ),
            (
                WithinRadiusQuery(
                    self.db,
                    JUPITER,
                    LIBRA.central_star,
                    LIBRA.radius,
                    EclipticPosition.BEHIND,
                    SearchRange.for_night(month, 4),
                ),
                Category.PLANETARY,
            ),
        ]

        return self.category_filter(res)

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
        res: List[Tuple[AbstractQuery, Category]] = [
            #  Year 9, month II, the 9th, last appearance behind α Leonis.
            (
                PlanetaryEventQuery(
                    self.db,
                    MARS,
                    OuterPlanetPhenomena.LA,
                    SearchRange.for_night(month, 9),
                ),
                Category.PLANETARY,
            ),
            (
                WithinRadiusQuery(
                    self.db,
                    MARS,
                    REGULUS,
                    15,
                    EclipticPosition.BEHIND,
                    SearchRange.for_night(month, 9),
                ),
                Category.PLANETARY,
            ),
        ]

        return self.category_filter(res)

    def year_9(self, nisan_1: float) -> List[MonthResult]:
        month_ii = self.repeat_month_with_alternate_starts(
            nisan_1, 2, self.year_9_month_2
        )
        return [month_ii]

    def __init__(self, data: AstroData, db: Database, subquery: Optional[str]):
        if subquery is None:
            self.filter = None
        elif subquery == "eclipse":
            self.filter = Category.ECLIPSE
        elif subquery == "lunar_six":
            self.filter = Category.LUNAR_SIX
        elif subquery == "planet":
            self.filter = Category.PLANETARY
        else:
            raise ValueError("Unknown subquery")
        tests = [
            YearToTest(0, "Cambyses 7", Intercalary.ADDARU, self.year_7),
            YearToTest(1, "Cambyses 8", Intercalary.FALSE, self.year_8),
            YearToTest(2, "Cambyses 9", Intercalary.FALSE, self.year_9),
        ]
        title = (
            "Cambyses 7"
            if self.filter is None
            else "Cambyses 7 ({})".format(self.filter.value)
        )
        super().__init__(data, db, tests, title)
