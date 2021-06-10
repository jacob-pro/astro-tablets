from enum import unique, Enum

from data import *
from generate.angular_separation import EclipticPosition
from generate.planet_events import OuterPlanetPhenomena, InnerPlanetPhenomena
from query.abstract_query import AbstractQuery, SearchRange
from query.abstract_tablet import AbstractTablet, PotentialMonthResult, YearToTest, Intercalary
from query.angular_separation_query import AngularSeparationQuery
from query.database import BabylonianDay
from query.lunar_eclipse_query import LunarEclipseQuery, ExpectedEclipseType, FirstContactTime, FirstContactRelative
from query.lunar_six_query import LunarSixQuery, LunarSix
from query.planetary_event_query import PlanetaryEventQuery


@unique
class BM33066Mode(Enum):
    ALL = "All"
    ECLIPSE_ONLY = "Eclipses Only"
    LUNAR_SIX_ONLY = "Lunar Six Only"
    PLANET_ONLY = "Planetary Only"


class BM33066(AbstractTablet):

    def year_7_month_1(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.LUNAR_SIX_ONLY:
            res.append(LunarSixQuery(self.db, month, 1, LunarSix.NA1, 30))
            res.append(LunarSixQuery(self.db, month, 13, LunarSix.ME, 9))
            res.append(LunarSixQuery(self.db, month, 13, LunarSix.SU2, 2.5))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.GI6, 8 + 1/3))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.NA, 7 + 2/3))
            res.append(LunarSixQuery(self.db, month, 27, LunarSix.KUR, 16))

        return res

    def year_7_month_2(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.LUNAR_SIX_ONLY:
            res.append(LunarSixQuery(self.db, month, 1, LunarSix.NA1, 23))
            res.append(LunarSixQuery(self.db, month, 13, LunarSix.SU2, 8 + 2/3))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.ME, 1))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.NA, 1 + 2/3))
            res.append(LunarSixQuery(self.db, month, 15, LunarSix.GI6, 14.5))
            res.append(LunarSixQuery(self.db, month, 27, LunarSix.KUR, 21))

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.PLANET_ONLY:
            res.append(PlanetaryEventQuery(self.db, MARS, OuterPlanetPhenomena.LA, SearchRange.for_night(month, 28)))
            res.append(AngularSeparationQuery(self.db, MARS, GEMINI.central_star, 0, GEMINI.radius,
                                              EclipticPosition.AHEAD, SearchRange.for_night(month, 28)))

        return res

    def year_7_month_3(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.LUNAR_SIX_ONLY:
            res.append(LunarSixQuery(self.db, month, 1, LunarSix.NA1, 18.5))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.ME, 9.5))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.SU2, 4))
            res.append(LunarSixQuery(self.db, month, 15, LunarSix.GI6, 5))
            res.append(LunarSixQuery(self.db, month, 15, LunarSix.NA, 8.5))
            res.append(LunarSixQuery(self.db, month, 27, LunarSix.KUR, 15))

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.PLANET_ONLY:
            res.append(PlanetaryEventQuery(self.db, VENUS, InnerPlanetPhenomena.EL, SearchRange.for_night(month, 10)))
            res.append(AngularSeparationQuery(self.db, VENUS, LEO.central_star, 0, LEO.radius,
                                              None, SearchRange.for_night(month, 10)))
            res.append(PlanetaryEventQuery(self.db, VENUS, InnerPlanetPhenomena.MF, SearchRange.for_night(month, 27)))
            res.append(AngularSeparationQuery(self.db, VENUS, CANCER.central_star, 0, CANCER.radius,
                                              None, SearchRange.for_night(month, 27)))


        return res

    def year_7_month_4(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.LUNAR_SIX_ONLY:
            res.append(LunarSixQuery(self.db, month, 1, LunarSix.NA1, 27))
            res.append(LunarSixQuery(self.db, month, 13, LunarSix.SU2, 11))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.ME, 4))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.NA, 4))
            res.append(LunarSixQuery(self.db, month, 15, LunarSix.GI6, 8.5))
            res.append(LunarSixQuery(self.db, month, 27, LunarSix.KUR, 15))

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.ECLIPSE_ONLY:
            t = (1 + 2/3) * 30
            res.append(LunarEclipseQuery(self.db, FirstContactTime(t, FirstContactRelative.AFTER_SUNSET),
                                         ExpectedEclipseType.TOTAL, None, None,
                                         SearchRange.for_night(month, 14)))

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.PLANET_ONLY:
            # Year 7, month IV, the 1st, the moon became visible 3 cubits behind Mercury.
            res.append(AngularSeparationQuery(self.db, MOON, MERCURY, 3 * CUBIT, 1 * CUBIT,
                                              EclipticPosition.BEHIND, SearchRange.for_night(month, 1)))

        return res

    def year_7_month_5(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.LUNAR_SIX_ONLY:
            res.append(LunarSixQuery(self.db, month, 1, LunarSix.NA1, 10, low_precision=True))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.SU2, 3.5))
            res.append(LunarSixQuery(self.db, month, 15, LunarSix.ME, 2.5, low_precision=True))
            res.append(LunarSixQuery(self.db, month, 15, LunarSix.NA, 11))
            res.append(LunarSixQuery(self.db, month, 16, LunarSix.GI6, 7.5))
            res.append(LunarSixQuery(self.db, month, 27, LunarSix.KUR, 22.5))

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.PLANET_ONLY:
            res.append(PlanetaryEventQuery(self.db, JUPITER, OuterPlanetPhenomena.LA, SearchRange.for_night(month, 22)))
            res.append(AngularSeparationQuery(self.db, JUPITER, VIRGO.central_star, 0, VIRGO.radius,
                                              EclipticPosition.AHEAD, SearchRange.for_night(month, 22)))

        return res

    def year_7_month_6(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.LUNAR_SIX_ONLY:
            res.append(LunarSixQuery(self.db, month, 1, LunarSix.NA1, 15 + 2/3))
            res.append(LunarSixQuery(self.db, month, 13, LunarSix.SU2, 11))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.NA, 4))
            res.append(LunarSixQuery(self.db, month, 15, LunarSix.ME, 1 + 1/3))
            res.append(LunarSixQuery(self.db, month, 16, LunarSix.GI6, 8 + 2/3))
            res.append(LunarSixQuery(self.db, month, 27, LunarSix.KUR, 15))

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.PLANET_ONLY:
            res.append(PlanetaryEventQuery(self.db, JUPITER, OuterPlanetPhenomena.FA, SearchRange.for_night(month, 22)))
            res.append(AngularSeparationQuery(self.db, JUPITER, VIRGO.central_star, 0, VIRGO.radius,
                                              EclipticPosition.BEHIND, SearchRange.for_night(month, 22)))
            res.append(PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.LA, SearchRange.for_night(month, 3)))
            res.append(AngularSeparationQuery(self.db, SATURN, VIRGO.central_star, 0, VIRGO.radius,
                                              None, SearchRange.for_night(month, 3)))
            res.append(PlanetaryEventQuery(self.db, MARS, OuterPlanetPhenomena.FA, SearchRange.for_night(month, 13)))
            res.append(AngularSeparationQuery(self.db, MARS, LEO.central_star, 0, LEO.radius,
                                              None, SearchRange.for_night(month, 13)))

            #  Month VI, the 24th, Venus was 1 +[x cubits?] above Mars.
            res.append(AngularSeparationQuery(self.db, VENUS, MARS, 1 * CUBIT, 5 * CUBIT,
                                              EclipticPosition.ABOVE, SearchRange.for_night(month, 24)))

        return res

    def year_7_month_7(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.LUNAR_SIX_ONLY:
            res.append(LunarSixQuery(self.db, month, 1, LunarSix.NA1, 16 + 2/3))
            res.append(LunarSixQuery(self.db, month, 13, LunarSix.SU2, 6.5))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.ME, 7.5))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.NA, 12))
            res.append(LunarSixQuery(self.db, month, 15, LunarSix.GI6, 3))
            res.append(LunarSixQuery(self.db, month, 26, LunarSix.KUR, 22))

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.PLANET_ONLY:
            res.append(PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.FA, SearchRange.for_night(month, 13)))
            res.append(AngularSeparationQuery(self.db, SATURN, VIRGO.central_star, 0, VIRGO.radius,
                                              EclipticPosition.BEHIND, SearchRange.for_night(month, 13)))

            # Month VII, the 23rd, last part of the night, Jupiter was 3 cubits above the moon.
            res.append(AngularSeparationQuery(self.db, JUPITER, MOON, 3 * CUBIT, 1 * CUBIT,
                                              EclipticPosition.ABOVE, SearchRange.for_night(month, 23)))

            # Month VII, the 29th, last part of the night, Venus on the north side [came near?] 2 fingers to Ju[piter].
            res.append(AngularSeparationQuery(self.db, VENUS, JUPITER, 2 * FINGER, 2 * FINGER,
                                              None, SearchRange.for_night(month, 29)))

            # Month VII, the 12th, Saturn was 1 cubit in front of Jupiter.
            res.append(AngularSeparationQuery(self.db, SATURN, JUPITER, 1 * CUBIT, 6 * FINGER,
                                              EclipticPosition.AHEAD, SearchRange.for_night(month, 12)))

            # Month VII, the 11th, Mars came near to Jupiter 2 fingers.
            res.append(AngularSeparationQuery(self.db, MARS, JUPITER, 2 * FINGER, 2 * FINGER,
                                              None, SearchRange.for_night(month, 11)))

        return res

    def year_7_month_8(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.LUNAR_SIX_ONLY:
            res.append(LunarSixQuery(self.db, month, 1, LunarSix.NA1, 12 + 2/3))
            res.append(LunarSixQuery(self.db, month, 13, LunarSix.SU2, 15))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.NA, 5))
            res.append(LunarSixQuery(self.db, month, 15, LunarSix.ME, 1))
            res.append(LunarSixQuery(self.db, month, 16, LunarSix.GI6, 14))
            res.append(LunarSixQuery(self.db, month, 28, LunarSix.KUR, 26))

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.PLANET_ONLY:
            # Month VIII, the 2nd, Saturn passed 8 fingers above Venus.
            res.append(AngularSeparationQuery(self.db, SATURN, VENUS, 8 * FINGER, 4 * FINGER,
                                              EclipticPosition.ABOVE, SearchRange.for_night(month, 2)))

        return res

    def year_7_month_10(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.ECLIPSE_ONLY:
            t = (2 + 1 / 2) * 30
            res.append(LunarEclipseQuery(self.db, FirstContactTime(t, FirstContactRelative.BEFORE_SUNRISE),
                                         ExpectedEclipseType.TOTAL, None, None,
                                         SearchRange.for_night(month, 14)))

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.PLANET_ONLY:
            res.append(PlanetaryEventQuery(self.db, JUPITER, OuterPlanetPhenomena.ST, SearchRange.for_night(month, 27)))
            res.append(AngularSeparationQuery(self.db, JUPITER, LIBRA.central_star, 0, LIBRA.radius,
                                              EclipticPosition.AHEAD, SearchRange.for_night(month, 27)))

            # Month X, the 5th, Mercury was ½ cubit behind Venus.
            res.append(AngularSeparationQuery(self.db, MERCURY, VENUS, 0.5 * CUBIT, 6 * FINGER,
                                              EclipticPosition.BEHIND, SearchRange.for_night(month, 5)))

        return res

    def year_7_month_11(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.LUNAR_SIX_ONLY:
            res.append(LunarSixQuery(self.db, month, 1, LunarSix.NA1, 22))
            res.append(LunarSixQuery(self.db, month, 13, LunarSix.ME, 17 + 1/3))
            res.append(LunarSixQuery(self.db, month, 13, LunarSix.SU2, 4 + 2/3))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.GI6, 1 + 2/3))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.NA, 7))
            res.append(LunarSixQuery(self.db, month, 27, LunarSix.KUR, 17))

        return res

    def year_7_month_12(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.LUNAR_SIX_ONLY:
            res.append(LunarSixQuery(self.db, month, 1, LunarSix.NA1, 15.5))
            res.append(LunarSixQuery(self.db, month, 12, LunarSix.SU2, 10.5))
            res.append(LunarSixQuery(self.db, month, 13, LunarSix.ME, 5 + 1/3))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.GI6, 10))
            res.append(LunarSixQuery(self.db, month, 25, LunarSix.KUR, 23))
            res.append(LunarSixQuery(self.db, month, 27, LunarSix.KUR, 12))

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.PLANET_ONLY:
            res.append(PlanetaryEventQuery(self.db, VENUS, InnerPlanetPhenomena.ML, SearchRange.for_night(month, 7)))
            res.append(AngularSeparationQuery(self.db, VENUS, PISCES.central_star, 0, PISCES.radius,
                                              None, SearchRange.for_night(month, 7)))

        return res

    def year_7_month_13(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.LUNAR_SIX_ONLY:
            res.append(LunarSixQuery(self.db, month, 1, LunarSix.NA1, 19))
            res.append(LunarSixQuery(self.db, month, 13, LunarSix.ME, 1.5, low_precision=True))
            res.append(LunarSixQuery(self.db, month, 13, LunarSix.SU2, 5 + 1/3))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.GI6, 3))
            res.append(LunarSixQuery(self.db, month, 14, LunarSix.NA, 5 + 2/3))
            res.append(LunarSixQuery(self.db, month, 27, LunarSix.KUR, 21))

        return res

    def year_7(self, nisan_1: float) -> List[PotentialMonthResult]:
        month_i = self.repeat_month_with_alternate_starts(nisan_1, 1, self.year_7_month_1)
        month_ii = self.repeat_month_with_alternate_starts(nisan_1, 2, self.year_7_month_2)
        month_iii = self.repeat_month_with_alternate_starts(nisan_1, 3, self.year_7_month_3)
        month_iv = self.repeat_month_with_alternate_starts(nisan_1, 4, self.year_7_month_4)
        month_v = self.repeat_month_with_alternate_starts(nisan_1, 5, self.year_7_month_5)
        month_vi = self.repeat_month_with_alternate_starts(nisan_1, 6, self.year_7_month_6)
        month_vii = self.repeat_month_with_alternate_starts(nisan_1, 7, self.year_7_month_7)
        month_viii = self.repeat_month_with_alternate_starts(nisan_1, 8, self.year_7_month_8)
        month_x = self.repeat_month_with_alternate_starts(nisan_1, 10, self.year_7_month_10)
        month_xi = self.repeat_month_with_alternate_starts(nisan_1, 11, self.year_7_month_11)
        month_xii = self.repeat_month_with_alternate_starts(nisan_1, 12, self.year_7_month_12)
        month_xii2 = self.repeat_month_with_alternate_starts(nisan_1, 13, self.year_7_month_13)

        return [month_i, month_ii, month_iii, month_iv, month_v, month_vi, month_vii, month_viii, month_x, month_xi,
                month_xii, month_xii2]


    def year_8_month_1(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.PLANET_ONLY:
            res.append(PlanetaryEventQuery(self.db, VENUS, InnerPlanetPhenomena.EF, SearchRange.for_night(month, 13)))
            res.append(AngularSeparationQuery(self.db, VENUS, AURIGA.central_star, 0, AURIGA.radius,
                                              None, SearchRange.for_night(month, 13)))

        return res

    def year_8_month_2(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.PLANET_ONLY:
            res.append(PlanetaryEventQuery(self.db, JUPITER, OuterPlanetPhenomena.ST, SearchRange.for_night(month, 25)))
            res.append(AngularSeparationQuery(self.db, JUPITER, VIRGO.central_star, 0, VIRGO.radius,
                                              None, SearchRange.for_night(month, 25)))

        return res

    def year_8_month_5(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.PLANET_ONLY:
            res.append(PlanetaryEventQuery(self.db, SATURN, OuterPlanetPhenomena.LA, SearchRange.for_night(month, 29)))
            res.append(PlanetaryEventQuery(self.db, MARS, OuterPlanetPhenomena.ST, SearchRange.for_night(month, 12)))

        return res

    def year_8_month_6(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.PLANET_ONLY:
            res.append(PlanetaryEventQuery(self.db, JUPITER, OuterPlanetPhenomena.LA, SearchRange.for_night(month, 4)))
            res.append(AngularSeparationQuery(self.db, JUPITER, LIBRA.central_star, 0, LIBRA.radius,
                                              EclipticPosition.BEHIND, SearchRange.for_night(month, 4)))

        return res

    def year_8(self, nisan_1: float) -> List[PotentialMonthResult]:
        month_i = self.repeat_month_with_alternate_starts(nisan_1, 2, self.year_8_month_1)
        month_ii = self.repeat_month_with_alternate_starts(nisan_1, 2, self.year_8_month_2)
        month_v = self.repeat_month_with_alternate_starts(nisan_1, 5, self.year_8_month_5)
        month_vi = self.repeat_month_with_alternate_starts(nisan_1, 6, self.year_8_month_6)
        return [month_i, month_ii, month_v, month_vi]


    def year_9_month_2(self, month: List[BabylonianDay]) -> List[AbstractQuery]:
        res = []

        if self.mode == BM33066Mode.ALL or self.mode == BM33066Mode.PLANET_ONLY:
            res.append(PlanetaryEventQuery(self.db, MARS, OuterPlanetPhenomena.LA, SearchRange.for_night(month, 9)))
            res.append(AngularSeparationQuery(self.db, MARS, REGULUS, 0, 15,
                                              EclipticPosition.BEHIND, SearchRange.for_night(month, 9)))

        return res

    def year_9(self, nisan_1: float) -> List[PotentialMonthResult]:
        month_ii = self.repeat_month_with_alternate_starts(nisan_1, 2, self.year_9_month_2)
        return [month_ii]

    def do_query(self, subquery: Union[str, None], print_year: Union[int, None], slim_results: bool):
        if subquery == "eclipse_only":
            self.mode = BM33066Mode.ECLIPSE_ONLY
        elif subquery == "lunar_six_only":
            self.mode = BM33066Mode.LUNAR_SIX_ONLY
        elif subquery == "planet_only":
            self.mode = BM33066Mode.PLANET_ONLY
        else:
            self.mode = BM33066Mode.ALL
        tests = [YearToTest(0, "Cambyses 7", Intercalary.ADDARU, self.year_7),
                 YearToTest(1, "Cambyses 8", Intercalary.FALSE, self.year_8),
                 YearToTest(2, "Cambyses 9", Intercalary.FALSE, self.year_9)]
        res = self.run_years(tests)
        self.print_results(res, "Cambyses 7 ({})".format(self.mode.value))
        self.output_json_for_year(res, print_year, slim_results)
